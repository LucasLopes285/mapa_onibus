from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Onibus
from backend.schemas import OnibusSchema  # 🔹 Importando schema atualizado
from backend.security import verificar_admin

router = APIRouter()

# 🔹 Criar um novo ônibus (linha)
@router.post("/onibus", response_model=OnibusSchema)
def criar_onibus(onibus: OnibusSchema, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    onibus_existente = db.query(Onibus).filter(Onibus.nome == onibus.nome).first()
    if onibus_existente:
        raise HTTPException(status_code=400, detail="Já existe uma linha de ônibus com esse nome")

    novo_onibus = Onibus(
        nome=onibus.nome,  # 🔹 Substituímos "placa" por "nome" da linha
        rota_id=onibus.rota_id,
        paradas=onibus.paradas
    )

    db.add(novo_onibus)
    db.commit()
    db.refresh(novo_onibus)
    return novo_onibus

# 🔹 Listar todas as linhas de ônibus
@router.get("/onibus", response_model=list[OnibusSchema])
def listar_onibus(db: Session = Depends(get_db)):
    return db.query(Onibus).all()

# 🔹 Buscar uma linha de ônibus específica 
@router.get("/onibus/nome/{onibus_nome}", response_model=OnibusSchema)
def buscar_onibus(onibus_nome: str, db: Session = Depends(get_db)):
    onibus = db.query(Onibus).filter(Onibus.nome.ilike(f"%{onibus_nome}%")).first()
    if not onibus:
        raise HTTPException(status_code=404, detail="Linha de ônibus não encontrada")
    return onibus

# 🔹 Atualizar os dados de uma linha de ônibus
@router.put("/onibus/{onibus_id}", response_model=OnibusSchema)
def atualizar_onibus(onibus_id: int, onibus_update: OnibusSchema, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    onibus = db.query(Onibus).filter(Onibus.id == onibus_id).first()
    if not onibus:
        raise HTTPException(status_code=404, detail="Linha de ônibus não encontrada")

    # Atualizando os campos
    onibus.nome = onibus_update.nome  # 🔹 Atualizamos o nome da linha, não a placa
    onibus.rota_id = onibus_update.rota_id
    onibus.paradas = onibus_update.paradas

    db.commit()
    db.refresh(onibus)
    return onibus

# 🔹 Excluir uma linha de ônibus
@router.delete("/onibus/{onibus_id}")
def excluir_onibus(onibus_id: int, db: Session = Depends(get_db), usuario=Depends(verificar_admin)):
    onibus = db.query(Onibus).filter(Onibus.id == onibus_id).first()
    if not onibus:
        raise HTTPException(status_code=404, detail="Linha de ônibus não encontrada")
    db.delete(onibus)
    db.commit()
    return {"message": "Linha de ônibus excluída com sucesso"}
