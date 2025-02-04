from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Parada
from pydantic import BaseModel
from models import Usuario
from routes.usuarios import verificar_admin


router = APIRouter()

# Modelo para criação ou atualização de uma parada
class ParadaSchema(BaseModel):
    nome: str
    coordenadas: dict
    descricao: str

# Listar todas as paradas
@router.get("/paradas")
def listar_paradas(db: Session = Depends(get_db)):
    return db.query(Parada).all()

# Criar uma nova parada
@router.post("/paradas")
def criar_parada(parada: ParadaSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    nova_parada = Parada(nome=parada.nome, coordenadas=parada.coordenadas, descricao=parada.descricao)
    db.add(nova_parada)
    db.commit()
    db.refresh(nova_parada)
    return nova_parada

# Atualizar uma parada existente
@router.put("/paradas/{parada_id}")
def atualizar_parada(parada_id: int, parada: ParadaSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    parada_db = db.query(Parada).filter(Parada.id == parada_id).first()
    if not parada_db:
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    parada_db.nome = parada.nome
    parada_db.coordenadas = parada.coordenadas
    parada_db.descricao = parada.descricao
    db.commit()
    db.refresh(parada_db)
    return parada_db

# Excluir uma parada
@router.delete("/paradas/{parada_id}")
def excluir_parada(parada_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    parada_db = db.query(Parada).filter(Parada.id == parada_id).first()
    if not parada_db:
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    db.delete(parada_db)
    db.commit()
    return {"message": "Parada excluída com sucesso"}