from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class FormularioInput(BaseModel):
    mensagem: str

class FormularioOutput(BaseModel):
    resposta: str

def processa_mensagem(mensagem: str) -> str:
    # Aqui pode chamar LLM, ou qualquer lógica
    if "sinistro" in mensagem.lower():
        return "Entendi, você quer registrar um sinistro. Qual o seu CPF?"
    else:
        return "Desculpe, não entendi. Pode reformular?"

@app.post("/messages-upsert", response_model=FormularioOutput)
def preencher(dados: FormularioInput):
    resposta = processa_mensagem(dados.mensagem)
    return {"resposta": resposta}
