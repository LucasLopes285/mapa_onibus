from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.rotas import router as rotas_router
from backend.routes.paradas import router as paradas_router
from backend.routes.usuarios import router as usuarios_router
from backend.routes.onibus import router as onibus_router  # Se houver

app = FastAPI()

# 🔹 Configuração correta do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔹 Se estiver rodando localmente, ajuste a porta conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # 🔹 Permitir todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # 🔹 Permitir todos os headers
)

# 🔹 Registrar as rotas
app.include_router(rotas_router, prefix="/api", tags=["Rotas"])
app.include_router(paradas_router, prefix="/api", tags=["Paradas"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuários"])
app.include_router(onibus_router, prefix="/api", tags=["Ônibus"])  
