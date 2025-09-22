"""
Módulo de Handlers (Manipuladores) de Comandos.

Aqui reside a lógica de negócio para cada comando que o bot pode executar.
Cada função recebe o payload validado do webhook e executa uma ação,
geralmente chamando uma ou mais funções do módulo de serviços.
"""
import logging
from src.models.evolution import WebhookPayload
from src.services import evolution_api
from src.infra.config import settings

logger = logging.getLogger(__name__)

async def handle_ping(payload: WebhookPayload):
    """
    Handler para o comando /ping. Responde com 'pong'.
    """
    instance_name = payload.instance
    chat_id = payload.data.key.remote_jid
    response_text = "pong"

    logger.info(f"Executando comando /ping para o chat {chat_id}")
    
    evolution_api.send_text_message(
        instance=instance_name,
        to_number=chat_id,
        text=response_text
    )

# async def handle_delete_message(payload: WebhookPayload):
#     """
#     Handler para o comando /excluir.
#     Deleta a mensagem que foi respondida pelo comando.
#     """
#     # Para o comando /excluir funcionar, o utilizador deve responder (citar)
#     # a mensagem que deseja apagar ao enviar o comando.
#     # A informação da mensagem citada está dentro de 'extendedTextMessage'.
#     msg_content = payload.data.message
#     if not (msg_content and msg_content.extended_text_message):
#         evolution_api.send_text_message(
#             instance=payload.instance,
#             to_jid=payload.data.key.remote_jid,
#             text="⚠️ Para usar o comando /excluir, você deve responder à mensagem que deseja apagar."
#         )
#         return

#     # Extraímos os detalhes da mensagem citada
#     quoted_msg_context = msg_content.extended_text_message.get("contextInfo", {})
#     quoted_msg_id = quoted_msg_context.get("stanzaId")
#     quoted_msg_participant = quoted_msg_context.get("participant")

#     if not all([quoted_msg_id, quoted_msg_participant]):
#         logger.warning("Não foi possível extrair os detalhes da mensagem a ser excluída.")
#         return

#     logger.info(f"Executando comando /excluir para a mensagem {quoted_msg_id}")

#     # Montamos o objeto 'key' da mensagem a ser deletada
#     key_to_delete = {
#         "remoteJid": payload.data.key.remote_jid,
#         "id": quoted_msg_id,
#         "participant": quoted_msg_participant
#     }

#     evolution_api.delete_message(instance=payload.instance, message_key=key_to_delete)

#     # Opcional: Apagar também a mensagem de comando ("/excluir")
#     key_of_command_msg = payload.data.key.dict(by_alias=True)
#     evolution_api.delete_message(instance=payload.instance, message_key=key_of_command_msg)


# async def handle_unrecognized_command(payload: WebhookPayload):
#     """
#     Handler para quando um comando não é reconhecido.
#     """
#     logger.info(f"Comando não reconhecido recebido de {payload.data.key.participant}")
#     evolution_api.send_text_message(
#         instance=payload.instance,
#         to_jid=payload.data.key.remote_jid,
#         text="😕 Comando não reconhecido. Tente /ping ou /excluir."
#     )
