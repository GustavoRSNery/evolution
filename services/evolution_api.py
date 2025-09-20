"""
Módulo de Serviço para Interagir com a Evolution API.

Este arquivo centraliza toda a lógica de comunicação de SAÍDA para a
API da Evolution. Se a API deles mudar no futuro, este será o único
lugar que precisaremos modificar.

Cada função aqui representa uma ação que o nosso bot pode realizar.
"""
import requests
import logging
from infra.config import settings  # Importa as nossas configurações centralizadas

logger = logging.getLogger(__name__)

# --- Funções de Envio de Mensagens ---

def send_text_message(instance: str, to_jid: str, text: str) -> dict | None:
    """
    Envia uma mensagem de texto simples para um utilizador ou grupo.

    Args:
        instance: O nome da instância da Evolution API.
        to_jid: O JID do destinatário (ex: "12345@g.us" ou "5511999998888@s.whatsapp.net").
        text: O conteúdo da mensagem a ser enviada.

    Returns:
        Um dicionário com a resposta da API em caso de sucesso, ou None em caso de erro.
    """
    endpoint = f"{settings.EVOLUTION_API_URL}/message/sendText/{instance}"
    headers = {"apikey": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"}
    payload = {
        "number": to_jid,
        "options": {"delay": 1200, "presence": "composing"},
        "textMessage": {"text": text},
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)
        logger.info(f"Mensagem de texto enviada com sucesso para {to_jid}.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Falha ao enviar mensagem de texto para {to_jid}: {e}")
        return None

# --- Funções de Moderação ---

def delete_message(instance: str, message_key: dict) -> bool:
    """
    Deleta uma mensagem para todos no chat.

    Args:
        instance: O nome da instância da Evolution API.
        message_key: O objeto 'key' da mensagem a ser deletada, contendo
                     remoteJid, id, e participant.

    Returns:
        True se a mensagem foi deletada com sucesso, False caso contrário.
    """
    endpoint = f"{settings.EVOLUTION_API_URL}/message/delete/{instance}"
    headers = {"apikey": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"}
    
    # O payload para deletar uma mensagem é o próprio objeto 'key'
    payload = message_key

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Mensagem {message_key.get('id')} deletada com sucesso do chat {message_key.get('remoteJid')}.")
        # A API pode retornar diferentes respostas de sucesso, verificamos o status
        return response.status_code in [200, 201]
    except requests.RequestException as e:
        logger.error(f"Falha ao deletar a mensagem {message_key.get('id')}: {e}")
        return False

# Poderíamos adicionar mais funções aqui no futuro, como:
# - send_quoted_message(...)
# - send_media_message(...)
# - get_group_info(...)
