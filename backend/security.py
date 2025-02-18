import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Usuario

# 🔹 Chave secreta para gerar o token JWT (agora usando variável de ambiente)
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔹 Configuração do bcrypt para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

# 🔹 Função para verificar se a senha está correta
def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

# 🔹 Função para criar hash de senha
def criar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

# 🔹 Função para criar token JWT
def criar_token_jwt(dados: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = dados.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Função para obter usuário autenticado
def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception
    return usuario

# 🔹 Função para verificar se o usuário é administrador
def verificar_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    usuario = obter_usuario_atual(token, db)
    if usuario.tipo != "administrador":
        raise HTTPException(status_code=403, detail="Acesso negado. Somente administradores podem realizar esta ação.")
    return usuario
