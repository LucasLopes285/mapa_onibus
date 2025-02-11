from fastapi import FastAPI
from backend.routes.rotas import router as rotas_router
from backend.routes.paradas import router as paradas_router
from backend.routes.usuarios import router as usuarios_router
from backend.database import engine
from backend.models import Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Incluindo os endpoints
app.include_router(rotas_router, prefix="/api", tags=["Rotas"])
app.include_router(paradas_router, prefix="/api", tags=["Paradas"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuários"])

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (substituir pelo domínio do frontend se necessário)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Permite todos os headers
)

@app.get("/")
def home():
    return {"mensagem": "API de Rotas de Ônibus funcionando!"}