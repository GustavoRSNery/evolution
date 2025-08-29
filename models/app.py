import requests
import os
from dotenv import load_dotenv

load_dotenv("D:\Projects\evolution\.env")
EVOLUTION_AUTH = os.getenv("AUTHENTICATION_API_KEY")

BASE_URL = "http://localhost:8080"
INSTANCE_NAME="" # o nome da instancia que foi colocada no /manager no site

NUMERO = "5562994980317"
MENSAGEM = "Testando api"

headers = {
    'apikey': EVOLUTION_AUTH,
    'Content-Type': 'application/json'
}
payload = {
    'number': f'{NUMERO}',
    'text': f'{MENSAGEM}',
    # 'delay': 10000, # simular "digitando"
}
response = requests.post(
    url=f'{BASE_URL}/message/sendText/{INSTANCE_NAME}',
    json=payload,
    headers=headers,
)
print(response.json())
