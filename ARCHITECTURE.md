# Guia da Arquitetura do Projeto - Bot WhatsApp

Este documento serve como um guia técnico detalhado sobre a arquitetura de software do projeto. O seu objetivo é explicar a responsabilidade de cada diretório e ficheiro, facilitando a manutenção, a escalabilidade e a integração de novos desenvolvedores.

O projeto adota uma arquitetura inspirada em **Ports and Adapters (Arquitetura Hexagonal)**, que promove uma forte separação de responsabilidades (Separation of Concerns).

---

## Estrutura de Alto Nível

O projeto está organizado numa estrutura de layout `src`, uma prática recomendada pela comunidade Python para separar o código-fonte da aplicação dos ficheiros de configuração e gestão do projeto.

```
/meu_bot_whatsapp/
├── 📂 src/                  # Contém todo o código-fonte da aplicação.
├── 📄 .env                   # Configurações de ambiente e segredos.
├── 📄 Dockerfile              # Receita para construir a imagem Docker da aplicação.
├── 📄 docker-compose.yml      # Orquestra todos os serviços (bot, API, DB, etc.).
├── 📄 main.py                 # Ponto de entrada da aplicação FastAPI.
├── 📄 requirements.txt        # Dependências Python.
├── 📄 CHANGELOG.md            # Registo de alterações do projeto.
└── 📄 ROADMAP.md              # Plano de funcionalidades futuras.
```

---

## Detalhes das Camadas (Dentro de `src/`)

O diretório `src/` contém o núcleo da nossa aplicação, dividido em camadas lógicas.

### `📂 api/` - A Camada de Apresentação (Porta de Entrada)

Esta camada é a única que "conversa" com o mundo exterior através do protocolo HTTP. A sua única responsabilidade é receber requisições, delegar para a camada de comandos e retornar uma resposta.

* **`api/v1/`**: Diretório que agrupa todos os endpoints da versão 1 da nossa API. Isto facilita o versionamento no futuro.
* **`api/v1/api.py`**: Funciona como o **agregador de rotas** da v1. Ele importa os roteadores de todos os ficheiros em `endpoints/` и os organiza sob um único `APIRouter`, definindo prefixos (ex: `/webhook`) e tags para a documentação.
* **`api/v1/endpoints/webhook.py`**: Define os endpoints HTTP reais. É aqui que criamos as rotas (`@router.post("/inspect")`), lidamos com a validação inicial (através dos `models`) e passamos a responsabilidade para a camada de comandos. Contém também a lógica do inspetor web (WebSocket e a página HTML).

### `📂 commands/` - A Camada de Lógica de Negócio (O Cérebro)

Esta é a camada central da aplicação, onde as decisões são tomadas. Ela não sabe o que é HTTP ou uma base de dados; apenas recebe dados validados e executa a lógica.

* **`router.py`**: Atua como um **dispatcher**. A sua função `dispatch` recebe um payload validado, analisa o conteúdo da mensagem para identificar um comando (ex: `/ping`) e o encaminha para a função `handler` correta. É aqui que regras de negócio, como ignorar mensagens do próprio bot (`fromMe: true`), são aplicadas.
* **`handlers.py`**: Contém as **funções que executam os comandos**. Cada comando tem a sua própria função (ex: `handle_ping`). É aqui que a lógica de "o que fazer" é implementada, como chamar um serviço para enviar uma resposta.

### `📂 core/` - A Camada de Configuração

Esta camada centraliza todas as configurações da aplicação.

* **`config.py`**: Utiliza a biblioteca `pydantic-settings`, que você gosta de usar, para carregar, validar e tipar as variáveis de ambiente a partir do ficheiro `.env`. Ele expõe um objeto `settings` que fornece acesso seguro e autocompletado a todas as configurações em qualquer parte do projeto.

### `📂 models/` - A Camada de Contrato de Dados

Esta camada define a "forma" dos dados com que a nossa aplicação trabalha.

* **`evolution.py`**: Contém as classes **Pydantic** que modelam os payloads dos webhooks. O FastAPI usa estes modelos para validar automaticamente as requisições recebidas, garantindo que a nossa camada de lógica de negócio só receba dados que estão no formato correto.

### `📂 services/` - A Camada de Serviços Externos

Esta camada isola toda a comunicação com o mundo exterior que não seja a recepção de webhooks.

* **`evolution_api.py`**: Atua como um **cliente HTTP** para a Evolution API. Todas as funções para interagir com a API (enviar mensagens, apagar mensagens, etc.) estão encapsuladas aqui. Se a Evolution API mudar no futuro, este é o único ficheiro que precisaremos de alterar.

### `📂 templates/` - A Camada de Visão (Templates)

Este diretório contém os ficheiros de "visão", como HTML.

* **`inspector.html`**: A página web do nosso inspetor de payloads. É um ficheiro estático que contém o HTML, CSS (Tailwind) e JavaScript (com lógica WebSocket) para o nosso visualizador em tempo real.

---

## Ficheiros na Raiz do Projeto

* **`main.py`**: O ponto de entrada da aplicação. A sua única responsabilidade é criar a instância do FastAPI e incluir o roteador principal da `api/v1/api.py`.
* **`Dockerfile`**: A "receita" que o Docker usa para construir a imagem do nosso bot. Ele define o sistema operativo base, instala as dependências do `requirements.txt` e copia o nosso código `src/` para dentro da imagem.
* **`docker-compose.yml`**: O "maestro" que orquestra todo o ambiente. Ele define todos os serviços (`bot-whatsapp-service`, `evolution-api`, `postgres`, `redis`), as suas configurações, as redes de comunicação e os volumes de dados.