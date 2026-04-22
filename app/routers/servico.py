from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.servico import (
    ServicoCreate,
    ServicoUpdate,
    ServicoResponse
)

from app.crud import servico as crud


router = APIRouter(
    prefix="/servicos",
    tags=["Servicos"]
)


@router.post("/", response_model=ServicoResponse)
def criar(servico: ServicoCreate, db: Session = Depends(get_db)):
    return crud.create_servico(db, servico)


@router.get("/", response_model=list[ServicoResponse])
def listar(db: Session = Depends(get_db)):
    return crud.get_servicos(db)


@router.get("/{servico_id}", response_model=ServicoResponse)
def pegar_por_id(servico_id: str, db: Session = Depends(get_db)):
    servico = crud.get_servico_by_id(db, servico_id)

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    return servico


@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar(
    servico_id: str,
    servico: ServicoUpdate,
    db: Session = Depends(get_db)
):
    servico_db = crud.update_servico(
        db,
        servico_id,
        servico
    )

    if not servico_db:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    return servico_db


@router.delete("/{servico_id}")
def deletar(servico_id: str, db: Session = Depends(get_db)):
    servico = crud.delete_servico(db, servico_id)

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    return {"message": "Serviço deletado com sucesso"}
