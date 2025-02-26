from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Rota, Usuario, Onibus
from backend.schemas import RotaSchema
from backend.security import verificar_admin  # 🔹 Agora garantimos que apenas administradores podem fazer alterações

router = APIRouter()

# 🔹 Listar todas as rotas (disponível para todos os usuários)
@router.get("/rotas", response_model=list[RotaSchema])
def listar_rotas(db: Session = Depends(get_db)):
    return db.query(Rota).all()

# 🔹 Buscar uma rota pelo nome (disponível para todos os usuários)
@router.get("/rotas/nome/{rota_nome}", response_model=RotaSchema)
def buscar_rota_por_nome(rota_nome: str, db: Session = Depends(get_db)):
    rota = db.query(Rota).filter(Rota.nome.ilike(f"%{rota_nome}%")).first()
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

@router.get("/rotas/{rota_id}", response_model=RotaSchema)
def buscar_rota_por_id(rota_id: int, db: Session = Depends(get_db)):
    rota = db.query(Rota).filter(Rota.id == rota_id).first()
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota


# 🔹 Criar uma nova rota (somente administradores)
@router.post("/rotas", response_model=RotaSchema)
def criar_rota(rota: RotaSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    if not rota.nome.strip():
        raise HTTPException(status_code=400, detail="O nome da rota não pode estar vazio.")
    
    # 🚀 Garantindo que os dados já são JSON e formatando corretamente
    try:
        pontos_json = [ponto.dict() for ponto in rota.pontos]
    except AttributeError:
        pontos_json = rota.pontos  # Se já estiver em JSON, usa diret

    # Criar a nova rota
    nova_rota = Rota(nome=rota.nome, pontos=pontos_json)
    db.add(nova_rota)
    db.commit()
    db.refresh(nova_rota)

    # Criar o ônibus associado à rota
    novo_onibus = Onibus(nome=rota.nome, rota_id=nova_rota.id, paradas=[])  # Lista vazia de paradas
    db.add(novo_onibus)
    db.commit()

    return nova_rota


# 🔹 Atualizar uma rota existente (somente administradores)
@router.put("/rotas/{rota_id}", response_model=RotaSchema)
def atualizar_rota(rota_id: int, rota: RotaSchema, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    rota_db = db.query(Rota).filter(Rota.id == rota_id).first()
    if not rota_db:
        raise HTTPException(status_code=404, detail="Rota não encontrada")

    rota_db.nome = rota.nome
    rota_db.pontos = [{"lat": p.lat, "lng": p.lng} for p in rota.pontos]

    db.commit()
    db.refresh(rota_db)
    return rota_db

# 🔹 Excluir uma rota (somente administradores)
@router.delete("/rotas/{rota_id}")
def excluir_rota(rota_id: int, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    rota_db = db.query(Rota).filter(Rota.id == rota_id).first()
    if not rota_db:
        raise HTTPException(status_code=404, detail="Rota não encontrada")

    db.delete(rota_db)
    db.commit()
    return {"message": "Rota excluída com sucesso"}
