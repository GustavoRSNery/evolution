"""
Ponto de entrada principal da aplicação FastAPI.

Este arquivo é responsável por:
1. Inicializar o objeto principal da aplicação FastAPI.
2. Configurar o logging básico para a aplicação.
3. Incluir os roteadores da API (neste caso, o roteador da v1).
4. Definir uma rota raiz ("/") para uma verificação de saúde (health check).

Para rodar esta aplicação:
1. Abra o terminal.
2. Ative o ambiente virtual: `source venv/bin/activate` (ou `.\venv\Scripts\activate` no Windows).
3. Execute o servidor uvicorn: `uvicorn main:app --reload`
"""
import logging
from fastapi import FastAPI
from api.v1.api import api_router  # Importa o agregador de rotas da v1

# --- Configuração do Logging ---
# Configura o logging para exibir mensagens de nível INFO e acima.
# Isso garante que os logs dos nossos módulos (ex: webhook.py) sejam visíveis no console.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# --- Inicialização da Aplicação ---
# Cria a instância principal da aplicação FastAPI.
# A documentação automática (Swagger UI) estará disponível em /docs
app = FastAPI(
    title="Bot de WhatsApp com Evolution API",
    description="Servidor de webhook para processar eventos e executar comandos.",
    version="1.0.0"
)

# --- Inclusão das Rotas da API ---
# Inclui todas as rotas definidas no 'api_router' (de api/v1/api.py)
# com o prefixo global '/v1'.
# Isso significa que a URL final do nosso webhook será:
# [URL_DO_NGROK] + /v1 + /webhook + /evolution
app.include_router(api_router, prefix="/v1")

# --- Rota Raiz (Health Check) ---
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar se a aplicação está online.
    """
    return {
        "status": "online",
        "message": "Servidor de Webhook para Evolution API está a funcionar!",
        "docs_url": "/docs"
    }

# Para executar, use o comando: uvicorn main:app --reload
