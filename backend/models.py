from sqlalchemy import Column, Integer, String, JSON
from backend.database import Base

# Modelo para a tabela de rotas
class Rota(Base):
    __tablename__ = "rotas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    pontos = Column(JSON, nullable=False)

# Modelo para a tabela de paradas
class Parada(Base):
    __tablename__ = "paradas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    coordenadas = Column(JSON, nullable=False)
    descricao = Column(String, nullable=True)

# Modelo para a tabela de usuários
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # 'administrador' ou 'usuario'
