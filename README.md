# 🔥 Quiz API - Sistema de Quiz sobre Prevenção de Incêndios

Uma API moderna e assíncrona para sistema de quiz educativo focado em prevenção de incêndios e queimadas, construída com **Quart** (async Flask) e **Oracle Database**.

## Equipe

- Fabrício Gomes – RM  558216
- Felipe Cerboncini – RM  554909
- Vitor Chaves – RM  557067

## ✨ Funcionalidades

- 🔐 **Autenticação JWT** completa com registro e login
- ❓ **Sistema de Quiz** com questões aleatórias
- 🏆 **Ranking** global de usuários
- 📊 **Pontuação** individual e estatísticas
- 📚 **Documentação automática** com Swagger UI
- 🛡️ **Sistema robusto de tratamento de erros**
- ⚡ **Performance assíncrona** com SQLAlchemy async
- 🧪 **Arquitetura limpa** com separation of concerns

## 🚀 Tecnologias

- **[Quart](https://quart.palletsprojects.com/)** - Framework web assíncrono
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM com suporte async
- **[Oracle Database](https://www.oracle.com/database/)** - Banco de dados
- **[JWT](https://jwt.io/)** - Autenticação stateless
- **[Quart-Schema](https://github.com/pgjones/quart-schema)** - Documentação OpenAPI/Swagger
- **[Hypercorn](https://hypercorn.readthedocs.io/)** - Servidor ASGI

## 📋 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- pip ou poetry

## ⚙️ Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/quiz-api.git
cd quiz-api
```

### 2. Crie o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o Oracle Database com Docker

O projeto já inclui um `docker-compose.yml` para subir o Oracle Database:

```bash
# Inicie o banco de dados Oracle
docker-compose up -d

# Aguarde alguns minutos para o banco inicializar completamente
# O healthcheck garantirá que o banco esteja pronto
```

O Docker Compose cria automaticamente:
- **Container:** `quiz_oracle` 
- **Database:** `quizdb`
- **Usuário:** `quiz_app` / `quiz123`
- **Porta:** `1521` (mapeada para localhost)

### 5. Variáveis de ambiente

O projeto já possui um arquivo `.env` configurado na raiz com todas as variáveis necessárias. As configurações padrão estão alinhadas com o Docker Compose.

> **📝 Nota:** Sempre passe o caminho do arquivo `.env` ao executar os scripts: `--env-file ../../.env`

## 🏃‍♂️ Como executar

### 1. Inicie o banco de dados
```bash
# Suba o Oracle Database via Docker
docker-compose up -d

# Verifique se o banco está rodando
docker-compose ps
```

### 2. Inicie a aplicação
```bash
cd app/api
python main.py --env-file ../../.env
```

### 3. Acesse a aplicação
- **API Base:** http://localhost:8000
- **Documentação:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

> **💡 Dica:** O banco pode levar alguns minutos para inicializar completamente. O healthcheck do Docker Compose garantirá que esteja pronto antes de usar.

## 📚 Populando o Banco de Dados

O projeto inclui um script para popular o banco com perguntas sobre prevenção de incêndios:

```bash
cd app/populate_db
python main.py --env-file ../../.env
```

Este script adiciona **12 questões** educativas sobre:
- Prevenção de incêndios domésticos
- Cuidados com queimadas
- Procedimentos de emergência
- Segurança com fogo

## 📖 Documentação da API

### Categorias de Endpoints

| Categoria | Descrição | Endpoints |
|-----------|-----------|-----------|
| 🔐 **Authentication** | Registro e login | `/api/auth/register`, `/api/auth/login` |
| ❓ **Quiz** | Questões e respostas | `/api/questions/random`, `/api/quiz/answer/{id}/{id}` |
| 👤 **User** | Perfil e pontuação | `/api/score` |
| 🏆 **Ranking** | Rankings globais | `/api/ranking` |
| 💚 **Health** | Status da API | `/health` |

### Autenticação

1. **Registre um usuário:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario123",
    "email": "user@example.com", 
    "password": "senha123",
    "password_confirmation": "senha123",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

2. **Faça login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario123",
    "password": "senha123"
  }'
```

3. **Use o token** nas requisições protegidas:
```bash
curl -X GET http://localhost:8000/api/questions/random \
  -H "Authorization: Bearer SEU_JWT_TOKEN"
```

### Exemplos de Uso

**Obter questão aleatória:**
```bash
GET /api/questions/random
Authorization: Bearer {token}
```

**Responder questão:**
```bash
POST /api/quiz/answer/{question_id}/{answer_id}
Authorization: Bearer {token}
```

**Ver pontuação:**
```bash
GET /api/score
Authorization: Bearer {token}
```

**Ver ranking:**
```bash
GET /api/ranking
```

## 🛡️ Sistema de Erros

A API possui um sistema robusto de tratamento de erros com:

- **Exceptions customizadas** por categoria (User, Quiz, Auth, etc.)
- **Handlers automáticos** que convertem exceptions em respostas HTTP
- **Códigos de erro padronizados** para facilitar debugging
- **Logging estruturado** por severidade

### Exemplos de Respostas de Erro

```json
{
  "error": "Bad Request",
  "message": "Password must be at least 6 characters",
  "error_code": "PASSWORD_TOO_SHORT"
}
```

```json
{
  "error": "Unauthorized", 
  "message": "Invalid username or password",
  "error_code": "INVALID_CREDENTIALS"
}
```

## 🔧 Configuração para Produção

Para ambiente de produção, configure as seguintes variáveis de ambiente:

```bash
FLASK_ENV=production
DEBUG=false
JWT_SECRET_KEY=sua-chave-super-secreta-aqui
ORACLE_HOST=seu-host-producao
ORACLE_USERNAME=usuario-producao
ORACLE_PASSWORD=senha-segura-producao
```

> **⚠️ Importante:** Nunca use as credenciais padrão do `.env` em produção!

## 📊 Features Principais

### 🎯 Sistema de Quiz Inteligente
- Questões aleatórias para evitar decoreba
- Múltiplas alternativas por questão
- Sistema de pontuação configurable
- Feedback imediato com resposta correta

### 🏆 Gamificação
- Ranking global de usuários
- Pontuação acumulativa
- Estatísticas de accuracy
- Histórico de performance

### 🔐 Segurança
- Autenticação JWT stateless
- Passwords hasheados (SHA-256)
- Validação rigorosa de inputs
- Rate limiting preparado (configurável)

### ⚡ Performance
- Arquitetura 100% assíncrona
- Conexões de banco otimizadas
- Logs limpos e configuráveis
- Startup rápido

## 🧪 Testando a API

### Comandos de Desenvolvimento

```bash
# Iniciar a API
cd app/api && python main.py --env-file ../../.env

# Popular o banco com questões de exemplo
cd app/populate_db && python main.py --env-file ../../.env

# Voltar para raiz do projeto
cd ../..
```

### Comandos Úteis do Docker

```bash
# Verificar status dos containers
docker-compose ps

# Ver logs do banco de dados
docker-compose logs oracle-db

# Parar o banco de dados
docker-compose down

# Reiniciar o banco (com rebuild se necessário)
docker-compose down && docker-compose up -d

# Conectar diretamente ao Oracle (para debugging)
docker exec -it quiz_oracle sqlplus quiz_app/quiz123@quizdb
```

### Health Check
```bash
curl http://localhost:8000/health
# Resposta: {"status": "healthy", "service": "quiz-api"}
```

### Documentação Interativa
Acesse http://localhost:8000/docs para:
- ✅ Testar todos os endpoints
- ✅ Ver schemas de request/response
- ✅ Entender a autenticação JWT
- ✅ Explorar as funcionalidades

## 🆘 Suporte

Para dúvidas ou problemas:

1. **Issues:** Abra uma issue no GitHub
2. **Documentação:** Acesse `/docs` quando a API estiver rodando
3. **Logs:** Verifique os logs da aplicação para debugging

---

**Desenvolvido com ❤️ para educação sobre prevenção de incêndios** 🔥🚒
