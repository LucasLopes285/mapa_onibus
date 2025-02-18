from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Parada
from backend.schemas import ParadaSchema  # 🔹 Agora usamos o schema correto
from backend.routes.usuarios import verificar_admin


router = APIRouter()

# 🔹 Listar todas as paradas
@router.get("/paradas", response_model=list[ParadaSchema])
def listar_paradas(db: Session = Depends(get_db)):
    return db.query(Parada).all()

# 🔹 Buscar uma parada pelo nome (nova funcionalidade)
@router.get("/paradas/nome/{parada_nome}", response_model=ParadaSchema)
def buscar_parada_por_nome(parada_nome: str, db: Session = Depends(get_db)):
    parada = db.query(Parada).filter(Parada.nome.ilike(f"%{parada_nome}%")).first()
    if not parada:
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    return parada

# 🔹 Criar uma nova parada (apenas administradores)
@router.post("/paradas", response_model=ParadaSchema)
def criar_parada(parada: ParadaSchema, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    nova_parada = Parada(
        nome=parada.nome,
        coordenadas={"lat": parada.coordenadas.lat, "lng": parada.coordenadas.lng},
        descricao=parada.descricao
    )
    db.add(nova_parada)
    db.commit()
    db.refresh(nova_parada)
    return nova_parada

# 🔹 Atualizar uma parada existente (apenas administradores)
@router.put("/paradas/{parada_id}", response_model=ParadaSchema)
def atualizar_parada(parada_id: int, parada: ParadaSchema, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    parada_db = db.query(Parada).filter(Parada.id == parada_id).first()
    if not parada_db:
        raise HTTPException(status_code=404, detail="Parada não encontrada")

    parada_db.nome = parada.nome
    parada_db.coordenadas = {"lat": parada.coordenadas.lat, "lng": parada.coordenadas.lng}
    parada_db.descricao = parada.descricao

    db.commit()
    db.refresh(parada_db)
    return parada_db

# 🔹 Excluir uma parada (apenas administradores)
@router.delete("/paradas/{parada_id}")
def excluir_parada(parada_id: int, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    parada_db = db.query(Parada).filter(Parada.id == parada_id).first()
    if not parada_db:
        raise HTTPException(status_code=404, detail="Parada não encontrada")

    db.delete(parada_db)
    db.commit()
    return {"message": "Parada excluída com sucesso"}
