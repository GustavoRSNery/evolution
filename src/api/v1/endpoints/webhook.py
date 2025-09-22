"""
Define o endpoint que recebe os webhooks da Evolution API.
(VERSÃO FINAL - CONECTADA AO DISPATCHER DE COMANDOS)
"""
import logging
import json
import datetime
import asyncio
import httpx
from collections import deque
from typing import List
from pathlib import Path
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import ValidationError
from src.infra.config import settings
from src.models.evolution import WebhookPayload
from src.commands.dispatcher import dispatch

logger = logging.getLogger(__name__)
router = APIRouter()
# --- ARMAZENAMENTO EM MEMÓRIA PARA O INSPETOR ---
# Usamos uma lista com um tamanho máximo para armazenar os últimos 20 payloads.

payload_history = deque(maxlen=30)
active_connections: List[WebSocket] = []

# --- FUNÇÕES AUXILIARES (recepcionista)---
async def broadcast_payload(payload_entry: dict):
    """Envia o novo payload para todos os clientes WebSocket conectados."""
    for connection in active_connections:
        await connection.send_json(payload_entry)

async def forward_to_processor(payload_dict: dict):
    """Envia um payload validado para o endpoint de processamento interno."""
    processor_url = f"{settings.INTERNAL_API_URL}/v1/webhook/process"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(processor_url, json=payload_dict)
            response.raise_for_status()
            logger.info("Payload encaminhado com sucesso para o processador de comandos.")
    except httpx.RequestError as e:
        logger.error(f"Falha ao encaminhar payload para o processador: {e}")

# --- ENDPOINT PÚBLICO PRINCIPAL ---
@router.post("/inspect",
    summary="Receber e Inspecionar Todos os Webhooks",
    description="Este é o ponto de entrada principal. Ele aceita QUALQUER webhook, regista-o para depuração e o encaminha para processamento se for válido.",
    status_code=200
)
async def inspect_and_delegate_payload(request: Request):
    """
    Recebe, regista, transmite via WebSocket e, se válido, encaminha para processamento.
    """
    payload_dict = {}
    try:
        payload_dict = await request.json()
    except json.JSONDecodeError:
        logger.warning("Webhook recebido com corpo não-JSON.")
        return {"status": "ignored_non_json_payload"}

    # 1. Regista e transmite CADA payload que chega.
    payload_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "payload": payload_dict
    }
    payload_history.appendleft(payload_entry)
    await broadcast_payload(payload_entry)
    
    # 2. Tenta validar o payload contra o nosso schema de comandos.
    try:
        WebhookPayload.model_validate(payload_dict)
        # Se a validação for bem-sucedida, envia para a lógica de comandos em segundo plano.
        asyncio.create_task(forward_to_processor(payload_dict))
    except ValidationError:
        # Se a validação falhar (ex: áudio, status), apenas regista e ignora.
        logger.info(f"Payload recebido mas não corresponde a um schema de comando. A ignorar o processamento.")
    
    return {"status": "payload_received"}


# --- ENDPOINT DE INTERNO ---
@router.post("/process",
    summary="Processar um Webhook de Comando Validado",
    description="[INTERNO] Este endpoint só deve ser chamado pelo serviço. Ele executa a lógica de comandos.",
    include_in_schema=False # Oculta este endpoint da documentação pública.
)
async def process_validated_webhook(payload: WebhookPayload):
    """
    Contém a lógica de negócio para executar comandos.
    """
    logger.info(f"A processar webhook validado: Evento='{payload.event}', Instância='{payload.instance}'.")
    try:
        await dispatch(payload)
        return {"status": "command_processed_successfully"}
    except Exception as e:
        logger.error(f"Erro ao processar comando do evento '{payload.event}': {e}", exc_info=True)
        return {"status": "error_processing_command"}


# --- ENDPOINTS DO VISUALIZADOR WEB ---
@router.get("/inspect/history",
    summary="Histórico de Payloads",
    description="Retorna os últimos 30 payloads recebidos em formato JSON.",
)
async def get_inspection_history():
    return list(payload_history)

@router.get("/inspect/view",
    summary="Visualizador de Payloads",
    description="Serve uma página HTML para visualizar os webhooks em tempo real.",
    response_class=HTMLResponse
)
async def serve_inspector_page():
    """Serve a página HTML do inspetor a partir de um ficheiro externo."""
    html_file_path = Path("src/templ/inspector.html")
    if not html_file_path.is_file():
        return HTMLResponse(content="<h1>500 - Ficheiro do template não encontrado.</h1>", status_code=500)
    return HTMLResponse(content=html_file_path.read_text(encoding="utf-8"))

@router.websocket("/inspect/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para o visualizador de payloads."""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info("Novo cliente WebSocket conectado ao inspetor.")
    try:
        while True:
            # Mantém a conexão viva.
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("Cliente WebSocket desconectado.")