"""
Módulo de Configuração Centralizado.

Utiliza Pydantic Settings para carregar e validar as variáveis de ambiente
de um arquivo .env, tornando-as acessíveis de forma segura e tipada
em toda a aplicação.

Para usar, basta importar o objeto 'settings':
from core.config import settings
print(settings.EVOLUTION_API_URL)
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Define e valida as variáveis de ambiente necessárias para a aplicação.
    """
    # Configuração para carregar variáveis de um arquivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Configurações da Evolution API
    EVOLUTION_API_URL: str
    AUTHENTICATION_API_KEY: str
    INTERNAL_API_URL: str

    # Configurações do Bot
    TARGET_GROUP_ID: str

# Instância única das configurações que será importada por outros módulos.
settings = Settings()
