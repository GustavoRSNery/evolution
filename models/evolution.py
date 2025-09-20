"""
Define os modelos de dados (schemas) para os webhooks da Evolution API usando Pydantic.

Estes modelos são usados pelo FastAPI para:
1.  **Validação Automática:** Garantir que os dados recebidos na API correspondem à
    estrutura esperada. Se não corresponderem, o FastAPI retorna um erro 422
    automaticamente.
2.  **Conversão de Tipos:** Converter os dados JSON para objetos Python tipados.
3.  **Documentação:** Gerar schemas detalhados na documentação interativa (/docs),
    mostrando exatamente o que a API espera receber.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# --- Modelos Aninhados ---
# Estes modelos representam as partes internas do JSON do webhook.

class MessageKey(BaseModel):
    """
    Modela o objeto 'key' dentro do webhook, que contém os identificadores da mensagem.
    """
    remote_jid: str = Field(..., alias="remoteJid", description="ID do chat (grupo ou utilizador). Ex: 123456@g.us")
    from_me: bool = Field(..., alias="fromMe", description="Indica se a mensagem foi enviada pela instância do bot.")
    id: str = Field(..., description="ID único da mensagem.")
    participant: Optional[str] = Field(None, description="ID do participante que enviou a mensagem (apenas em grupos).")

class MessageContent(BaseModel):
    """
    Modela o conteúdo de uma mensagem de texto simples.
    O objeto 'message' pode ser muito complexo, então modelamos apenas o que precisamos.
    """
    conversation: Optional[str] = Field(None, description="Conteúdo da mensagem de texto.")
    # Adicionamos um campo genérico para capturar outras estruturas de mensagem sem causar erros.
    extended_text_message: Optional[Dict[str, Any]] = Field(None, alias="extendedTextMessage")


# --- Modelos Principais ---

class MessageData(BaseModel):
    """
    Modela o objeto 'data' para o evento 'messages.upsert'.
    """
    key: MessageKey
    message: Optional[MessageContent] = Field(None, description="O conteúdo da mensagem em si.")
    # Adicionamos um campo para capturar o timestamp da mensagem
    message_timestamp: int = Field(..., alias="messageTimestamp", description="Timestamp Unix de quando a mensagem foi recebida.")


class WebhookPayload(BaseModel):
    """
    Modelo de alto nível para o corpo (payload) de um webhook do evento 'messages.upsert'.
    Este é o modelo que o nosso endpoint de API irá esperar receber.
    """
    event: str = Field(..., description="Nome do evento. Ex: 'messages.upsert'")
    instance: str = Field(..., description="Nome da instância da Evolution API que enviou o evento.")
    data: MessageData = Field(..., description="Os dados específicos do evento.")
    # O remetente (sender) pode estar fora do objeto 'data' em alguns eventos
    sender: str = Field(..., description="O JID do remetente da instância da Evolution API.")

    class Config:
        # Permite que o Pydantic mapeie nomes em camelCase (como 'remoteJid')
        # para nomes em snake_case (como 'remote_jid') nos nossos modelos.
        populate_by_name = True
