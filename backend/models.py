from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.database import Base

# 🔹 Tabela intermediária para relação Many-to-Many entre Ônibus e Paradas
onibus_paradas_associacao = Table(
    "onibus_paradas",
    Base.metadata,
    Column("onibus_id", Integer, ForeignKey("onibus.id", ondelete="CASCADE"), primary_key=True),
    Column("parada_id", Integer, ForeignKey("paradas.id", ondelete="CASCADE"), primary_key=True)
)

# 🔹 Modelo para a tabela de rotas
class Rota(Base):
    __tablename__ = "rotas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    pontos = Column(JSON, nullable=False)  # 🔹 Lista de coordenadas para a rota

    onibus = relationship("Onibus", back_populates="rota")  # 🔹 Relacionamento com ônibus

# 🔹 Modelo para a tabela de paradas
class Parada(Base):
    __tablename__ = "paradas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    coordenadas = Column(JSON, nullable=False)  # 🔹 Latitude e longitude
    descricao = Column(String, nullable=True)

    onibus = relationship("Onibus", secondary=onibus_paradas_associacao, back_populates="paradas")

# 🔹 Modelo para a tabela de usuários
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # 🔹 'administrador' ou 'usuario'

# 🔹 Modelo para a tabela de ônibus
class Onibus(Base):
    __tablename__ = "onibus"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), unique=True, nullable=False)
    rota_id = Column(Integer, ForeignKey("rotas.id", ondelete="CASCADE"), nullable=False)

    rota = relationship("Rota", back_populates="onibus")  # 🔹 Relacionamento com a rota
    paradas = relationship("Parada", secondary=onibus_paradas_associacao, back_populates="onibus")  # 🔹 Many-to-Many com Paradas
