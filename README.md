# Bot de WhatsApp com Evolution API

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Versão](https://img.shields.io/badge/versão-0.1.0-blue)
![Licença](https://img.shields.io/badge/licença-MIT-green)

Um servidor de webhook modular, robusto e totalmente containerizado para a **Evolution API**, construído com FastAPI e Python. Este projeto serve como uma base sólida para a criação de bots de WhatsApp complexos, com um foco especial em ferramentas de depuração e boas práticas de engenharia de software, incluindo o uso de Pydantic, que você gosta de usar.

---

## 📜 Índice

* [Sobre o Projeto](#-sobre-o-projeto)
* [✨ Funcionalidades Principais](#-funcionalidades-principais)
* [🛠️ Stack Tecnológico](#️-stack-tecnológico)
* [🏗️ Arquitetura](#️-arquitetura)
* [🚀 Como Começar](#-como-começar)
  * [Pré-requisitos](#pré-requisitos)
  * [Instalação](#instalação)
* [🕹️ Como Usar](#️-como-usar)
  * [1. Expor o Bot com Ngrok](#1-expor-o-bot-com-ngrok)
  * [2. Configurar o Webhook](#2-configurar-o-webhook)
  * [3. Usar o Inspetor Web](#3-usar-o-inspetor-web)
  * [4. Comandos Disponíveis](#4-comandos-disponíveis)
* [🗺️ Roadmap](#️-roadmap)
* [🤝 Contribuindo](#-contribuindo)
* [📄 Licença](#-licença)

---

## 📖 Sobre o Projeto

Este projeto foi desenhado para ser uma fundação escalável para a automação do WhatsApp. Em vez de um único script, ele utiliza uma arquitetura de microsserviços orquestrada com Docker, separando claramente as responsabilidades para facilitar a manutenção e a adição de novas funcionalidades.

O seu principal diferencial é um **sistema de inspeção de webhooks em tempo real**, que permite visualizar 100% do tráfego enviado pela Evolution API através de uma interface web, facilitando a depuração e o desenvolvimento de novas funcionalidades.

## ✨ Funcionalidades Principais

* **Arquitetura Hexagonal:** Código organizado em camadas (API, Comandos, Modelos, Serviços) para alta manutenibilidade.
* **Ambiente 100% Dockerizado:** Configuração completa com `docker-compose` para subir todo o ambiente com um único comando.
* **Processador de Comandos:** Um sistema de `dispatcher` que analisa mensagens de texto e as encaminha para `handlers` específicos.
* **Inspetor de Payloads em Tempo Real:** Um visualizador web que utiliza WebSockets para exibir todos os webhooks recebidos (texto, áudio, imagens, status) sem a necessidade de olhar para o terminal.
* **Validação de Dados Robusta:** Utilização intensiva de modelos Pydantic para validar, serializar e documentar os dados da API.

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.12, FastAPI
* **Containerização:** Docker, Docker Compose
* **Comunicação em Tempo Real:** WebSockets
* **Validação de Dados:** Pydantic
* **Serviços de Suporte:** PostgreSQL, Redis
* **API Externa:** Evolution API

## 🏗️ Arquitetura

O projeto segue uma arquitetura de software limpa, separando o código em diretórios com responsabilidades bem definidas. Para uma explicação detalhada de cada pasta e ficheiro, consulte o nosso guia de arquitetura.

➡️ **[Ver o Guia de Arquitetura Detalhado](ARCHITECTURE.md)**

## 🚀 Como Começar

Siga estes passos para ter o projeto a rodar na sua máquina local.

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose
* Uma instância da [Evolution API](https://github.com/EvolutionAPI/evolution-api) a rodar (este projeto já a inclui no `docker-compose.yml`).
* [Ngrok](https://ngrok.com/) para expor a sua aplicação localmente.

### Instalação

1.  **Clone o repositório:** # Concluir esta parte da documentação
    ```bash
    git clone ...
    cd nome-do-projeto
    ```

2.  **Crie o seu ficheiro de configuração:**
    Copie o ficheiro de exemplo `.env.example` para um novo ficheiro chamado `.env`.
    ```bash
    cp .env.example .env
    ```

3.  **Preencha as suas variáveis de ambiente:**
    Abra o ficheiro `.env` num editor de texto e preencha todas as variáveis, especialmente a sua `EVOLUTION_API_KEY`, `AUTHENTICATION_API_KEY` e `TARGET_GROUP_ID`.

4.  **Suba o ambiente Docker:**
    Este comando irá construir a imagem do bot e iniciar todos os contêineres em segundo plano.
    ```bash
    docker-compose up --build -d
    ```

Após alguns momentos, todo o ambiente estará no ar!

## 🕹️ Como Usar

### 1. Expor o Bot com Ngrok

O nosso bot está a rodar na porta `8000`. Use o Ngrok para criar um túnel público para ele.
```bash
ngrok http 8000

.........
PASSAR ISTO PARA .MD
"""
Copie a URL https que o Ngrok fornecer (ex: https://aleatorio.ngrok-free.app).

2. Configurar o Webhook
Configure a sua Evolution API para enviar os webhooks para o nosso endpoint de inspeção. Isto garante que vejamos todos os eventos.

URL do Webhook: https://SUA_URL_NGROK.ngrok-free.app/v1/webhook/inspect

Você pode fazer isto através da interface da Evolution API ou com o comando PowerShell que usámos anteriormente.

3. Usar o Inspetor Web
Abra o seu navegador e aceda ao endereço do visualizador para ver os payloads em tempo real:

URL do Visualizador: https://SUA_URL_NGROK.ngrok-free.app/v1/webhook/inspect/view

4. Comandos Disponíveis
/ping: Envie esta mensagem num grupo (de um número de telemóvel que não seja o do bot) para testar se o bot está a responder. Ele deverá responder com pong.

🗺️ Roadmap
Temos muitas ideias para o futuro deste projeto! Você pode ver o nosso plano de desenvolvimento e as próximas funcionalidades no nosso roadmap.

➡️ Ver o Roadmap do Projeto

🤝 Contribuindo
Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será muito bem-vinda.

📄 Licença
Distribuído sob a Licença MIT. Veja LICENSE para mais informações.
"""

.......
EXEMPLO DE .ENV

"""
```text:Template de Variáveis de Ambiente:.env.example
# Este é um ficheiro de exemplo. Copie-o para um novo ficheiro chamado .env
# e preencha com os seus próprios valores. NUNCA envie o ficheiro .env para o Git.

# --- Configurações do Bot e da Evolution API ---

# A chave de API que o seu bot usará para se autenticar
EVOLUTION_API_KEY="SUA_CHAVE_API_AQUI"

# A chave de API que a Evolution API usará para se proteger
AUTHENTICATION_API_KEY="SUA_CHAVE_API_AQUI"

# O JID (ID do WhatsApp) do grupo que o bot deve monitorizar
# Exemplo: 120363041234567890@g.us
TARGET_GROUP_ID="SEU_ID_DE_GRUPO_AQUI@g.us"

# --- Configurações para os outros serviços ---

# URL da Evolution API (usada pelo nosso bot)
# O nome 'evolution-api' é resolvido pela rede interna do Docker.
EVOLUTION_API_URL="http://evolution-api:8080"

# URL interna do nosso próprio bot (usada para o 'eco' do inspetor)
INTERNAL_API_URL="http://bot-whatsapp-service:8000"

# Credenciais para a base de dados Postgres
# Estas variáveis são usadas tanto pelo contêiner do Postgres para se inicializar
# quanto pelo contêiner da Evolution API para se conectar.
POSTGRES_DB=evolution_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# --- Configurações internas da Evolution API ---
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?schema=public

CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI=redis://redis:6379
"""