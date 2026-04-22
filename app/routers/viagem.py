from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.viagem import (
    ViagemCreate,
    ViagemUpdate,
    ViagemResponse
)

from app.crud import viagem as viagem_crud
from app.core.database import get_db


router = APIRouter(
    prefix="/viagens",
    tags=["Viagens"]
)


@router.post("/", response_model=ViagemResponse)
def criar(viagem: ViagemCreate, db: Session = Depends(get_db)):
    return viagem_crud.create_viagem(db, viagem)




@router.get("/", response_model=list[ViagemResponse])
def listar(
    search: Optional[str] = None,
    data_inicio: Optional[str] = None,
    local_partida: Optional[str] = None,
    local_destino: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return viagem_crud.get_viagens(
        db,
        search=search,
        data_inicio=data_inicio,
        local_partida=local_partida,
        local_destino=local_destino,
        status=status
    )



@router.get("/{viagem_id}", response_model=ViagemResponse)
def buscar(viagem_id: str, db: Session = Depends(get_db)):
    viagem = viagem_crud.get_viagem_by_id(db, viagem_id)

    if not viagem:
        raise HTTPException(404, "Viagem não encontrada")

    return viagem


@router.put("/{viagem_id}", response_model=ViagemResponse)
def atualizar(
    viagem_id: str,
    viagem: ViagemUpdate,
    db: Session = Depends(get_db)
):
    viagem_updated = viagem_crud.update_viagem(db, viagem_id, viagem)

    if not viagem_updated:
        raise HTTPException(404, "Viagem não encontrada")

    return viagem_updated


@router.delete("/{viagem_id}")
def deletar(viagem_id: str, db: Session = Depends(get_db)):
    viagem_deleted = viagem_crud.delete_viagem(db, viagem_id)

    if not viagem_deleted:
        raise HTTPException(404, "Viagem não encontrada")

    return {"message": "Viagem deletada com sucesso"}