# Game Leaderboard API

API de backend em Python (Flask) desenvolvida para gerenciar o Top 10 mundial de um jogo 2D criado na Godot Engine. A arquitetura é totalmente conteinerizada com Docker e utiliza PostgreSQL para persistência segura dos dados.

## Tecnologias Utilizadas
* **Backend:** Python 3.13 (Debian Slim), Flask, Gunicorn
* **Banco de Dados:** PostgreSQL 15
* **Infraestrutura:** Docker, Docker Compose
* **Servidor (Produção):** Debian Linux (Headless)

---

## Estrutura do Projeto com Flask
```text
game-leaderboard-flask/
├── app/
│   ├── __init__.py      # Inicialização do Flask e Fábrica do App (Application Factory)
│   ├── config.py         # Configurações de ambiente
│   ├── database.py       # Funções de conexão com o banco SQLite
│   ├── routes.py         # As rotas/endpoints da API
│   └── validators.py     # Validação manual dos dados recebidos
├── docker-compose.yml    # Configurações para iniciar os containers
├── Dockerfile            # Configuração do container
├── .dockerignore         # Arquivos ignorados pelo Docker
└── requirements.txt      # Dependências do projeto
└── .gitignore
```
1. requirements.txt
    O Flask gerencia as rotas e o ciclo de vida HTTP. O Werkzeug é a biblioteca de utilitários WSGI que roda por baixo do Flask e cuida da segurança/servidor.

2. app/config.py
    • Centraliza as configurações do Flask. O Flask usa uma SECRET_KEY interna para sessões e segurança. Centralizar isso aqui evita expor dados sensíveis no código.

3. app/database.py
    O Flask possui um objeto chamado g (global de requisição). Ele serve para armazenar dados que duram apenas enquanto aquela requisição HTTP está acontecendo. Usar get_db e close_db garante que seu banco não sofra com arquivos travados ou vazamento de memória.

4. app/validators.py
    Como o Flask não possui validação automática nativa (como o Pydantic do FastAPI), criamos uma camada de validação manual. Ela impede que payloads corrompidos entrem no banco de dados.

5. app/routes.py
    O uso de Blueprints no Flask permite separar as rotas do arquivo de inicialização principal. Se no futuro seu jogo tiver um sistema de login, você pode criar um auth_bp sem bagunçar este arquivo de pontuação.

6. app/__init__.py
    O padrão Application Factory (create_app) é a forma profissional de iniciar o Flask. Ele evita importações circulares e permite criar instâncias isoladas do seu app para testes locais ou produção de forma limpa.

## O Dockerfile para o Flask
    O Dockerfile mudará apenas o comando final para rodar o servidor embutido do Flask (voltado para desenvolvimento/testes locais) ou preparar o server de produção.

---

## Parte 1: Execução e Testes Locais

Para desenvolver ou testar este projeto localmente, não é necessário instalar o banco de dados na sua máquina física, pois o Docker orquestrará todo o ambiente.

### Clonar o Repositório
```bash
git clone [link]
```
### Acesse o diretório do projeto
```bash
cd game-leaderboard-flask
```

### Configurar Variáveis de Ambiente (.env)
Crie um arquivo chamado .env na raiz do projeto. Aviso: Nunca envie este arquivo para o repositório público.
```bash
POSTGRES_USER=game_admin
POSTGRES_PASSWORD=sua_senha_secreta_local
POSTGRES_DB=leaderboard_db
SECRET_KEY=cole_aqui_uma_chave_segura_gerada_pelo_python
DATABASE_URL=postgresql://game_admin:sua_senha_secreta_local@db:5432/leaderboard_db
```

### Iniciar a Infraestrutura (Docker)
O Docker fará o download da imagem base otimizada, instalará as dependências do requirements.txt e conectará a API Flask ao PostgreSQL
```bash
docker compose up -d --build
```
Para verificar se os serviços subiram corretamente, utilize o comando docker ps. A API estará operando em http://localhost:8000.

### Testes de Validação (cURL)
Teste o endpoint de envio de pontuação:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/scores \
     -H "Content-Type: application/json" \
     -d '{"player_name": "LocalTester", "score": 9999}'
```

---

## Parte 2: Versionamento no GitHub
O projeto já contém um .gitignore configurado para impedir o vazamento do .env, chaves de segurança e ambientes virtuais locais (venv).

### Salvar as Modificações
```bash
git init
git add .
git commit -m "configuração da arquitetura de produção com Gunicorn, PostgreSQL e Docker"
```

### 2. Enviar para o GitHub
Crie um repositório no GitHub (sem inicializar com README) e vincule-o ao código local:
```bash
git branch -M main
git remote add origin [link]
git push -u origin main
```

---

## Parte 3: Deploy no Servidor de Produção (Debian)
O deploy é baseado em clonar o código atualizado e instruir o Docker a refazer a imagem, mantendo os dados preservados em volumes.

### Acesso Remoto
Acesse seu servidor local (ou nuvem) via SSH:
```Bash
ssh usuario@ip_do_servidor_debian
```

### Download do Código
```Bash
git clone [link]
cd game-leaderboard-flask
```
(Se o repositório for privado, autentique o servidor via Chave SSH ou Personal Access Token do GitHub).

### Configurar Credenciais de Produção
Crie o arquivo de variáveis de ambiente diretamente no servidor, utilizando senhas fortes reais para o banco de dados.
```Bash
nano .env
```
(Cole o conteúdo do .env, altere as senhas, salve com Ctrl+O / Enter e saia com Ctrl+X).

### Iniciar os Serviços Online
Inicie o ambiente de produção em segundo plano:
```Bash
docker compose up -d --build
```

### Rotina de Atualização Contínua
Sempre que você criar novas rotas no Manjaro e enviar para o GitHub, entre no servidor Debian e rode:
```Bash
git pull origin main
docker compose up -d --build
```
A API será reiniciada com o código novo em instantes. Os recordes e jogadores já cadastrados não serão perdidos, pois estão seguros no volume postgres_data.
