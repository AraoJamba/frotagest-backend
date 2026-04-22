from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
import bcrypt

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/eu")
def me(access_token: str = Cookie(None)):
    return {"usuario_id": access_token}

@router.post("/login")
def login(
    dados: LoginSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    senha_valida = bcrypt.checkpw(
        dados.senha.encode(),
        usuario.senha.encode()
    )

    if not senha_valida:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    # Criar cookie
    response.set_cookie(
        key="access_token",
        value=str(usuario.id),
        httponly=True,
        secure=False,  # True em produção
        samesite="lax"
    )

    return {"message": "Login realizado com sucesso"}
