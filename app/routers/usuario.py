from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)

from app.crud import usuario as crud
from typing import Optional


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResponse)
def criar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)


@router.get("/", response_model=list[UsuarioResponse])
def listar(
    search: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    papel: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_usuarios(
        db,
        search,
        nome,
        email,
        papel
    )



@router.get("/{usuario_id}", response_model=UsuarioResponse)
def pegar_por_id(usuario_id: str, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_id(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar(
    usuario_id: str,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    usuario_db = crud.update_usuario(
        db,
        usuario_id,
        usuario
    )

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario_db


@router.delete("/{usuario_id}")
def deletar(usuario_id: str, db: Session = Depends(get_db)):
    usuario = crud.delete_usuario(db, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return {"message": "Usuário deletado com sucesso"}
