"""
Agregador de Rotas para a Versão 1 (v1) da API.

Este ficheiro funciona como o "painel de controlo" da nossa API, organizando
todos os grupos de endpoints (roteadores) num único local.
Isto torna a nossa aplicação modular e fácil de expandir no futuro.
"""
from fastapi import APIRouter
# Importa o roteador que contém os nossos endpoints de webhook e inspeção.
from src.api.v1.endpoints import webhook

# Cria um roteador principal para a v1 da nossa API
api_router = APIRouter()

# Inclui todas as rotas definidas no módulo 'webhook.py'.
# O prefixo '/webhook' é adicionado a todas as rotas daquele módulo.
# Isto significa que as URLs finais serão construídas da seguinte forma:
# [URL_DO_NGROK] + /v1 (do main.py) + /webhook (daqui) + /inspect (do webhook.py)
#
# Exemplos de URLs finais:
# -> https://aleatorio.ngrok.io/v1/webhook/inspect      <- Endpoint principal para receber webhooks
# -> https://aleatorio.ngrok.io/v1/webhook/inspect/view <- Página do visualizador web
api_router.include_router(
    webhook.router, 
    prefix="/webhook", 
    tags=["Webhook & Inspector"] # Agrupa estes endpoints na documentação interativa (/docs)
)

# Se no futuro tivéssemos endpoints para utilizadores, adicionaríamos aqui,
# mantendo o nosso código organizado:
#
# from src.api.v1.endpoints import users
# api_router.include_router(users.router, prefix="/users", tags=["Users"])

