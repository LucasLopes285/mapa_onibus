from fastapi import FastAPI
from routes.rotas import router as rotas_router
from routes.paradas import router as paradas_router
from routes.usuarios import router as usuarios_router
from models import Base

app = FastAPI()

# Incluindo os endpoints
app.include_router(rotas_router, prefix="/api", tags=["Rotas"])
app.include_router(paradas_router, prefix="/api", tags=["Paradas"])
app.include_router(usuarios_router, prefix="/api", tags=["Usuários"])


