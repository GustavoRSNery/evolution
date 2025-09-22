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
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any


class MessageKey(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    remote_jid: str = Field(..., alias="remoteJid")
    id: str
    participant: Optional[str] = None
    from_me: bool = Field(alias="fromMe")

class MessageContent(BaseModel):
    """
    Modela o conteúdo de uma mensagem de texto simples.
    O objeto 'message' pode ser muito complexo, então modelamos apenas o que precisamos.
    """
    model_config = ConfigDict(extra="ignore")
    conversation: Optional[str] = None
    extendedTextMessage: Optional[Dict[str, Any]] = None


# --- Modelos Principais ---

class MessageData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    key: MessageKey
    message: Optional[MessageContent] = None
    message_timestamp: int = Field(alias="messageTimestamp")
    push_name: Optional[str] = Field(None, alias="pushName")


class WebhookPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    instance: str
    event: str
    data: MessageData
    sender: Optional[str] = None
