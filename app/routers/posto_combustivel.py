from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.posto_combustivel import (
    PostoCombustivelCreate,
    PostoCombustivelUpdate,
    PostoCombustivelResponse
)
from app.crud import posto_combustivel as posto_crud


router = APIRouter(
    prefix="/postos",
    tags=["Postos Combustivel"]
)


@router.post("/", response_model=PostoCombustivelResponse)
def criar(posto: PostoCombustivelCreate, db: Session = Depends(get_db)):
    return posto_crud.create_posto(db, posto)


@router.get("/", response_model=list[PostoCombustivelResponse])
def listar(db: Session = Depends(get_db)):
    return posto_crud.get_postos(db)


@router.get("/{posto_id}", response_model=PostoCombustivelResponse)
def pegar_por_id(posto_id: str, db: Session = Depends(get_db)):
    posto = posto_crud.get_posto_by_id(db, posto_id)

    if not posto:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return posto


@router.put("/{posto_id}", response_model=PostoCombustivelResponse)
def atualizar(
    posto_id: str,
    posto: PostoCombustivelUpdate,
    db: Session = Depends(get_db)
):
    posto_atualizado = posto_crud.update_posto(db, posto_id, posto)

    if not posto_atualizado:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return posto_atualizado


@router.delete("/{posto_id}")
def deletar(posto_id: str, db: Session = Depends(get_db)):
    posto = posto_crud.delete_posto(db, posto_id)

    if not posto:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return {"message": "Posto deletado com sucesso"}
