from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Rota
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models import Usuario
from routes.usuarios import verificar_admin


router = APIRouter()

# Modelo para criação de rota
class RotaSchema(BaseModel):
    nome: str
    pontos: list[dict]

# Listar todas as rotas
@router.get("/rotas")
def listar_rotas(db: Session = Depends(get_db)):
    return db.query(Rota).all()

# Criar nova rota (somente administradores)
@router.post("/rotas")
def criar_rota(rota: RotaSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    nova_rota = Rota(nome=rota.nome, pontos=rota.pontos)
    db.add(nova_rota)
    db.commit()
    db.refresh(nova_rota)
    return nova_rota

# Atualizar uma rota (somente administradores)
@router.put("/rotas/{rota_id}")
def atualizar_rota(rota_id: int, rota: RotaSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    rota_db = db.query(Rota).filter(Rota.id == rota_id).first()
    if not rota_db:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    rota_db.nome = rota.nome
    rota_db.pontos = rota.pontos
    db.commit()
    db.refresh(rota_db)
    return rota_db

# Excluir uma rota (somente administradores)
@router.delete("/rotas/{rota_id}")
def excluir_rota(rota_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    rota_db = db.query(Rota).filter(Rota.id == rota_id).first()
    if not rota_db:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    db.delete(rota_db)
    db.commit()
    return {"message": "Rota excluída com sucesso"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/usuarios/login")

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/rotas")
def criar_rota_autenticada(rota: RotaSchema, db: Session = Depends(get_db), usuario: str = Depends(verificar_token)):
    # Somente administradores podem criar rotas
    return criar_rota(rota, db)