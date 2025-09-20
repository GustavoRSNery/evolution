"""
Define o endpoint que recebe os webhooks da Evolution API.
(VERSÃO FINAL - CONECTADA AO DISPATCHER DE COMANDOS)
"""
from fastapi import APIRouter, Body
import logging
from models.evolution import WebhookPayload
# CONEXÃO FINAL: Importamos a função que despacha os comandos.
from commands.dispatcher import dispatch

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/evolution",
    summary="Receber Webhook da Evolution API",
    description="Este é o ponto de entrada para todas as notificações da Evolution API.",
    tags=["Webhook v1"]
)
async def handle_evolution_webhook(payload: WebhookPayload = Body(...)):
    """
    Processa os webhooks recebidos, validando-os com Pydantic e
    delegando a lógica para o dispatcher de comandos.
    """
    logger.info(f"Webhook validado: Evento='{payload.event}', Instância='{payload.instance}'.")

    # --- PONTO DE DELEGAÇÃO ATIVADO ---
    try:
        # Passamos o objeto Python validado para o cérebro do bot.
        await dispatch(payload)
    except Exception as e:
        logger.error(f"Erro ao processar o evento '{payload.event}': {e}", exc_info=True)
        return {"status": "error_while_processing"}

    return {"status": "event_processed_successfully"}

