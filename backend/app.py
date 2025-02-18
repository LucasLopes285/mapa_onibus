from fastapi import FastAPI
from backend.routes.rotas import router as rotas_router
from backend.routes.paradas import router as paradas_router
from backend.routes.usuarios import router as usuarios_router
from backend.routes.onibus import router as onibus_router  # 🔹 Adicionado endpoint de ônibus
from backend.database import engine
from backend.models import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔹 Criar as tabelas no banco de dados caso ainda não existam
Base.metadata.create_all(bind=engine)

# 🔹 Incluindo os endpoints
app.include_router(rotas_router, prefix="/api", tags=["Rotas"])
app.include_router(paradas_router, prefix="/api", tags=["Paradas"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuários"])
app.include_router(onibus_router, prefix="/api", tags=["Ônibus"])  # 🔹 Adicionado endpoint de ônibus

# 🔹 Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 Permite todos as origens
    allow_credentials=True,
    allow_methods=["*"],  # 🔹 Permite todos os métodos necessários
    allow_headers=["*"],  # 🔹 Permite todos os headers
)

@app.get("/")
def home():
    return {"mensagem": "API de Rotas de Ônibus funcionando!"}
