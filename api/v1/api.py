"""
Agregador de Rotas para a Versão 1 (v1) da API.

Este roteador define a estrutura dos nossos caminhos de URL. A URL base
será fornecida pelo NGROK, e este arquivo organiza o que vem depois dela.
"""
from fastapi import APIRouter
from api.v1.endpoints import webhook

api_router = APIRouter()

# Inclui as rotas do módulo 'webhook.py' com o prefixo '/webhook'.
# Isso significa que a URL final será:
# [URL_DO_NGROK] + /v1 (do main.py) + /webhook (daqui) + /evolution (do webhook.py)
# -> https://aleatorio.ngrok.io/v1/webhook/evolution
api_router.include_router(webhook.router, prefix="/webhook")

