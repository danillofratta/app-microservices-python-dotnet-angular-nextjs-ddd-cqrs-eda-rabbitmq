# My DDD API - FastAPI + PostgreSQL

## Estrutura do projeto
- `app/` - Código da aplicação
  - `api/` - Rotas e dependências FastAPI (v1, v2)
  - `application/` - DTOs, mappers, services
  - `domain/` - Entidades e exceptions
  - `infra/` - Banco de dados, modelos e repositórios
  - `core/` - Configurações, JWT, logger
  - `middlewares/` - Logging e exception handler

- `tests/` - Testes unitários e de integração

## Instalação

1. Clonar projeto
```bash
git clone <repo_url>
cd myapi_full_project
```

2. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

<!-- 3. Configurar `.env`
```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/mydb
JWT_SECRET=supersecretkey
```

## Rodando com Docker
```bash
docker-compose up --build
```

API disponível em `http://localhost:8000`

## Testes
```bash
pytest -v
``` -->
