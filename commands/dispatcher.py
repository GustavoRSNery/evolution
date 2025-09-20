"""
Módulo Roteador de Comandos (Dispatcher).

Este é o controlador de tráfego para a lógica do bot. Ele recebe
o payload validado, analisa o conteúdo da mensagem e decide qual
função do módulo 'handlers' deve ser chamada.
"""
import logging
from models.evolution import WebhookPayload
from commands import handlers
from infra.config import settings

logger = logging.getLogger(__name__)

# Mapeia strings de comando para as suas funções de handler correspondentes.
# Adicionar um novo comando é tão simples quanto adicionar uma nova entrada aqui.
COMMANDS_MAP = {
    "/ping": handlers.handle_ping,
    "/excluir": handlers.handle_delete_message,
}

async def dispatch(payload: WebhookPayload):
    """
    Recebe um payload de webhook e o direciona para o handler de comando apropriado.
    """
    # --- Filtros Iniciais ---
    # Ignorar se não for do grupo alvo ou se for uma mensagem do próprio bot
    if payload.data.key.remote_jid != settings.TARGET_GROUP_ID or payload.data.key.from_me:
        return

    # Ignorar se a mensagem não tiver conteúdo de texto
    if not payload.data.message:
        return

    # Extrai o texto da mensagem, seja de uma 'conversation' ou 'extendedTextMessage'
    text = ""
    if payload.data.message.conversation:
        text = payload.data.message.conversation.strip().lower()
    elif payload.data.message.extended_text_message and payload.data.message.extended_text_message.get('text'):
        text = payload.data.message.extended_text_message.get('text').strip().lower()

    if not text:
        return

    # --- Lógica de Roteamento ---
    # Verifica se o texto começa com um prefixo de comando conhecido
    command_word = text.split()[0] # Pega a primeira palavra, ex: "/ping"

    handler = COMMANDS_MAP.get(command_word)

    if handler:
        await handler(payload)
    # Opcional: Responder a qualquer mensagem que comece com "/" mas não seja um comando conhecido.
    # elif command_word.startswith("/"):
    #     await handlers.handle_unrecognized_command(payload)
