# Marketplace FastAPI

API RESTful desenvolvida com FastAPI para um marketplace.

## Estrutura do Projeto

```
app/
  core/          # Configurações e segurança
  infra/         # Infraestrutura (DB, Redis)
  modules/       # Módulos da aplicação
    users/       # Módulo de usuários
  main.py        # Aplicação principal
```

## Requisitos

- Python 3.11+
- PostgreSQL
- Redis
- Docker e Docker Compose (opcional)

## Instalação

1. Clone o repositório

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente no arquivo `.env`

5. Execute as migrações:
```bash
alembic upgrade head
```

## Executando a Aplicação

### Com Docker Compose (Recomendado)

```bash
docker-compose up -d
```

A API estará disponível em `http://localhost:8000`

### Localmente

```bash
uvicorn app.main:app --reload
```

## Documentação

Após iniciar a aplicação, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Usuários

- `POST /api/users/` - Criar usuário
- `GET /api/users/{user_id}` - Obter usuário por ID
- `PUT /api/users/{user_id}` - Atualizar usuário
- `POST /api/users/login` - Login e obter token

## Desenvolvimento

### Criar uma nova migração

```bash
alembic revision --autogenerate -m "Descrição da migração"
alembic upgrade head
```

## Tecnologias

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- PostgreSQL
- Redis
- Docker



