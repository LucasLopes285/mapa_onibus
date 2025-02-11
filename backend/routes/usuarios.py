from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Usuario
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

# Configuração do esquema de autenticação para obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

# Configuração de hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do JWT
SECRET_KEY = "chave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelo para criar usuários
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str  # 'administrador' ou 'usuario'

# Função para hash de senhas
def hash_senha(senha: str):
    return pwd_context.hash(senha)

# Endpoint para registrar novos usuários
@router.post("/usuarios/registro")
def registrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    # Verificar se o email já está em uso
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha),
        tipo=usuario.tipo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário registrado com sucesso"}

# Modelo para login
class LoginSchema(BaseModel):
    email: str
    senha: str

# Função para verificar senha
def verificar_senha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)

# Função para criar token JWT
def criar_token_dados(dados: dict):
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({"exp": expiracao})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint para login
@router.post("/usuarios/login")
def login(usuario: LoginSchema, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not usuario_db:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    if not verificar_senha(usuario.senha, usuario_db.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = criar_token_dados({"sub": usuario_db.email})
    return {"access_token": token, "token_type": "bearer"}

def verificar_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario is None or usuario.tipo != "administrador":
            raise HTTPException(status_code=403, detail="Acesso negado. Somente administradores podem realizar esta ação.")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
