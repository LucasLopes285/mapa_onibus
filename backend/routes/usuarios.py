from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Usuario
from backend.schemas import UsuarioSchema, LoginSchema, UsuarioRespostaSchema
from backend.security import criar_hash_senha, verificar_senha, criar_token_jwt, verificar_admin, obter_usuario_atual

router = APIRouter()

# 🔹 Qualquer usuário pode se registrar, mas não como administrador
@router.post("/usuarios/registro")
def registrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

    if usuario.tipo.lower() == "administrador":
        raise HTTPException(status_code=403, detail="Você não pode se cadastrar como administrador")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=criar_hash_senha(usuario.senha),  # 🔹 Agora usando `criar_hash_senha()`
        tipo="usuario"
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário registrado com sucesso"}

# 🔹 Somente administradores podem cadastrar outro administrador
@router.post("/usuarios/admin")
def registrar_admin(usuario: UsuarioSchema, db: Session = Depends(get_db), admin=Depends(verificar_admin)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

    novo_admin = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=criar_hash_senha(usuario.senha),  # 🔹 Agora usando `criar_hash_senha()`
        tipo="administrador"
    )
    db.add(novo_admin)
    db.commit()
    db.refresh(novo_admin)
    return {"message": "Administrador registrado com sucesso"}

# 🔹 Login de usuário
@router.post("/usuarios/login")
def login(usuario: LoginSchema, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    token = criar_token_jwt({"sub": usuario_db.email})  # 🔹 Agora usando `criar_token_jwt()`
    return {"access_token": token, "token_type": "bearer"}

# 🔹 Obter informações do usuário logado
@router.get("/usuarios/me", response_model=UsuarioRespostaSchema)
def obter_usuario_logado(usuario: Usuario = Depends(obter_usuario_atual)):
    return usuario  # 🔹 Agora a resposta não inclui a senha
