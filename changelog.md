# Changelog - Bot de WhatsApp com Evolution API

## [0.1.0] - 2025-09-21 - Lançamento Inicial: Arquitetura Robusta e Ferramentas de Depuração

Esta é a primeira versão funcional da arquitetura do bot de webhook. O foco principal foi estabelecer uma base robusta, modular e escalável, juntamente com ferramentas de depuração eficientes que evoluíram significativamente ao longo do processo de desenvolvimento.

### ✨ Novas Funcionalidades (Features)

* **Arquitetura de Software Profissional (Hexagonal):**
    * O projeto foi estruturado utilizando princípios de "Ports and Adapters", com uma clara separação de responsabilidades entre as camadas:
        * `api`: A porta de entrada para o mundo exterior (endpoints HTTP).
        * `commands`: O cérebro do bot, contendo a lógica de negócio.
        * `models`: O "contrato" de dados, garantindo a integridade com Pydantic, que você gosta de usar.
        * `services`: A camada de comunicação com APIs externas (Evolution API).
        * `core`: O núcleo de configurações da aplicação.

* **Infraestrutura Completa com Docker e Docker Compose:**
    * Ambiente de desenvolvimento e produção 100% containerizado.
    * Orquestração de quatro serviços interdependentes: `bot-whatsapp-service`, `evolution-api`, `postgres`, e `redis`, todos comunicando-se através de uma rede Docker interna (`whatsapp-net`).

* **Processador de Comandos Inteligente:**
    * Implementação de um sistema de `dispatcher` que analisa o conteúdo de mensagens de texto recebidas.
    * Mapeamento de palavras-chave (ex: `/ping`) para funções `handler` específicas.
    * Implementação de uma regra de segurança crucial para ignorar mensagens do próprio bot (`fromMe: true`), prevenindo loops de resposta infinitos.

* **Sistema de Inspeção de Payloads em Tempo Real:**
    * **Endpoint de Captura Universal (`/inspect`):** Um endpoint de entrada que aceita **todos** os webhooks da Evolution API (texto, áudio, imagens, status de entrega/leitura) **sem validação prévia**. Isto garante que nenhum dado seja perdido e permite uma visibilidade completa do tráfego.
    * **Visualizador Web (`/inspect/view`):** Uma página HTML servida diretamente pelo FastAPI que exibe os payloads capturados.
    * **Atualizações em Tempo Real com WebSockets:** A página utiliza uma conexão WebSocket para receber e exibir novos payloads instantaneamente, eliminando a necessidade de recarregar a página e evitando a sobrecarga de rede que ocorria com o método de polling anterior.

### 🐞 Correções de Erros e Desafios Superados (Bug Fixes)

* **Estabilização do Ambiente Docker:**
    * Resolvido um problema crítico de reinicialização em loop da `evolution-api` ao garantir que todas as variáveis de ambiente necessárias (`DATABASE_PROVIDER`, `DATABASE_CONNECTION_URI`, etc.) fossem carregadas através do `env_file` no `docker-compose.yml`.
    * Corrigido um problema de autenticação na `evolution-api` ao identificar e adicionar a variável de ambiente correta (`AUTHENTICATION_API_KEY`) no ficheiro `.env`.

* **Depuração de Erros de Validação (`422 Unprocessable Entity`):**
    * Foi diagnosticado que o bot rejeitava qualquer payload que não fosse uma mensagem de texto simples (ex: áudios, status de entrega).
    * A arquitetura foi refatorada para que o endpoint de entrada (`/inspect`) aceitasse todos os payloads e só depois tentasse validá-los para processamento, resolvendo o ciclo de erros e retentativas da `evolution-api`.
    * Os modelos Pydantic foram iterativamente tornados mais flexíveis (ex: tornando os campos `message`, `pushName`, `sender` opcionais), permitindo que o bot aceite a variedade de estruturas de payload enviadas pela API sem falhar.

* **Resolução de Problemas de Sintaxe e Ferramentas:**
    * Superado um problema de compatibilidade com o terminal do Windows, onde o `curl` é um alias para `Invoke-WebRequest`. A sintaxe dos comandos de teste foi ajustada para a estrutura de `hashtable` do PowerShell.
    * Corrigido um erro de inicialização do bot (`PydanticUserError: "Config" and "model_config" cannot be used together`) ao refatorar os modelos Pydantic para usar exclusivamente a sintaxe moderna da v2.

### 🔄 Alterações e Refatorações (Changes & Refactoring)

* **Evolução da Ferramenta de Depuração:**
    * A ideia inicial de um contêiner separado para inspeção foi descartada para evitar a complexidade de gerir múltiplos túneis do Ngrok (`ERR_NGROK_108`).
    * A funcionalidade foi integrada ao bot principal, primeiro com um sistema de polling que sobrecarregava a rede, e finalmente refatorada para uma solução eficiente com WebSockets.

* **Arquitetura de "Eco" (Passive Listening):**
    * Implementada uma arquitetura elegante onde o endpoint público `/inspect` recebe todos os dados, os exibe, e depois encaminha uma cópia para um endpoint interno (`/process`) de forma assíncrona. Isto separa completamente a depuração da lógica de negócio.

* **Estrutura de Projeto Profissional (`src/` layout):**
    * Todo o código da aplicação foi movido para um diretório `src/`, seguindo as melhores práticas da comunidade Python.
    * Todos os `imports` foram ajustados para serem absolutos a partir da raiz do projeto (`from src...`), resolvendo múltiplos `ModuleNotFoundError` e tornando o código mais robusto e manutenível.

* **Melhoria da Documentação da API:**
    * Foram adicionados `summary`, `description` e `tags` aos endpoints FastAPI, melhorando significativamente a clareza da documentação interativa gerada automaticamente em `/docs`.