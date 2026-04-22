from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from typing import Optional

from app.schemas.veiculo import (
    VeiculoCreate,
    VeiculoResponse,
    VeiculoUpdate
)

from app.crud import veiculo as crud
from app.core.database import get_db

router = APIRouter(prefix="/veiculos", tags=["Veiculos"])

@router.post("/", response_model=VeiculoResponse)
def criar(veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    return crud.criar(db, veiculo)




@router.get("/", response_model=List[VeiculoResponse])
def listar(
    search: Optional[str] = None,
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    marca: Optional[str] = None,
    ano: Optional[str] = None,
    VIN: Optional[str] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.listar(
        db,
        search,
        placa,
        modelo,
        marca,
        ano,
        VIN,
        tipo
    )



@router.get("/{id}", response_model=VeiculoResponse)
def obter(id: str, db: Session = Depends(get_db)):
    veiculo = crud.obter(db, id)

    if not veiculo:
        raise HTTPException(404, "Veiculo não encontrado")

    return veiculo


@router.put("/{id}", response_model=VeiculoResponse)
def atualizar(
    id: str,
    dados: VeiculoUpdate,
    db: Session = Depends(get_db)
):
    return crud.atualizar(db, id, dados)


@router.delete("/{id}")
def deletar(id: str, db: Session = Depends(get_db)):
    crud.deletar(db, id)
    return {"message": "Deletado"}