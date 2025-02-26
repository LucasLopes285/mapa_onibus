from pydantic import BaseModel
from typing import List, Optional

# 🔹 Modelo para representar coordenadas (lat/lng)
class Coordenada(BaseModel):
    lat: float
    lng: float

# 🔹 Modelo para validar os dados das Rotas
class RotaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    pontos: List[dict]  # 🔹 Lista de coordenadas representando o trajeto

    class Config:
        orm_mode = True

# 🔹 Modelo para validar os dados das Paradas
class ParadaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    coordenadas: Coordenada  # 🔹 Uma coordenada única para a parada
    descricao: Optional[str] = None

    class Config:
        orm_mode = True

# 🔹 Modelo para validar os dados dos Ônibus
class OnibusSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    rota_id: int
    paradas: List[ParadaSchema]  # 🔹 Lista de paradas completas, e não apenas IDs

    class Config:
        orm_mode = True

# 🔹 Modelo para validar os dados dos Usuários (cadastro)
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str  # "administrador" ou "usuario"

    class Config:
        orm_mode = True

# 🔹 Modelo para resposta de usuário (sem senha)
class UsuarioRespostaSchema(BaseModel):
    id: int
    nome: str
    email: str
    tipo: str  # "administrador" ou "usuario"

    class Config:
        orm_mode = True

# 🔹 Modelo para validar os dados de Login
class LoginSchema(BaseModel):
    email: str
    senha: str
