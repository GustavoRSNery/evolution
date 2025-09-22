"""
Módulo de Serviço para Interagir com a Evolution API.

Este arquivo centraliza toda a lógica de comunicação de SAÍDA para a
API da Evolution. Se a API deles mudar no futuro, este será o único
lugar que precisaremos modificar.

Cada função aqui representa uma ação que o nosso bot pode realizar.
"""
from typing import Optional, Dict, Any
import requests
import logging
from src.infra.config import settings  # Importa as nossas configurações centralizadas

logger = logging.getLogger(__name__)

# --- Funções de Envio de Mensagens ---

def send_text_message(
    instance: str, 
    to_number: str, 
    text: str,
    quoted_message: Optional[Dict[str, Any]] = None
):
    """
    Envia uma mensagem de texto, com a opção de responder a uma mensagem anterior.
    
    Args:
        instance: O nome da instância da Evolution API.
        to_number: O JID do destinatário (grupo ou utilizador).
        text: O conteúdo da mensagem a ser enviada.
        quoted_message: Um dicionário opcional contendo os dados da mensagem a ser citada.
                        Ex: {"key": {"id": "message_id"}, "message": {"conversation": "original text"}}
    """
    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{instance}"
    
    # Monta a estrutura base do payload
    payload = {
        "number": to_number,
        "delay": 1200,
        "text": text,
    }

    # Se os dados de uma mensagem a ser citada forem fornecidos, adiciona-os ao payload
    if quoted_message:
        payload["quoted"] = quoted_message
    
    headers = {
        "apikey": settings.AUTHENTICATION_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lança um erro para respostas 4xx ou 5xx
        logger.info(f"Mensagem de texto enviada com sucesso para {to_number}. Resposta da API: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha ao enviar mensagem de texto para {to_number}: {e}")
        if e.response:
            # Adiciona um log mais detalhado do corpo da resposta em caso de erro
            logger.error(f"Detalhes do erro da API ({e.response.status_code}): {e.response.text}")
        return None

# def delete_message(instance: str, remote_jid: str, msg_id: str, participant_id: str):
#     """
#     Deleta uma mensagem para todos no chat.

#     Args:
#         instance: O nome da instância da Evolution API.
#         message_key: O objeto 'key' da mensagem a ser deletada, contendo
#                      remoteJid, id, e participant.

#     Returns:
#         True se a mensagem foi deletada com sucesso, False caso contrário.
#     """
#     endpoint = f"{settings.EVOLUTION_API_URL}/message/delete/{instance}"
#     headers = {"apikey": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"}
    
#     # O payload para deletar uma mensagem é o próprio objeto 'key'
#     payload = message_key

#     try:
#         response = requests.post(endpoint, json=payload, headers=headers)
#         response.raise_for_status()
#         logger.info(f"Mensagem {message_key.get('id')} deletada com sucesso do chat {message_key.get('remoteJid')}.")
#         # A API pode retornar diferentes respostas de sucesso, verificamos o status
#         return response.status_code in [200, 201]
#     except requests.RequestException as e:
#         logger.error(f"Falha ao deletar a mensagem {message_key.get('id')}: {e}")
#         return False

# # Poderíamos adicionar mais funções aqui no futuro, como:
# # - send_quoted_message(...)
# # - send_media_message(...)
# # - get_group_info(...)
