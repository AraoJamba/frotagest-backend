from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from typing import Optional

from sqlalchemy import func
from app.models.veiculo import Veiculo, TipoVeiculo

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


@router.get("/estatisticas/resumo")
def resumo_veiculos(db: Session = Depends(get_db)):

    total = db.query(func.count(Veiculo.id)).scalar()

    activos = db.query(func.count(Veiculo.id)).filter(
        Veiculo.ativo == True
    ).scalar()

    inactivos = db.query(func.count(Veiculo.id)).filter(
        Veiculo.ativo == False
    ).scalar()

    carros = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.carro
    ).scalar()

    caminhoes = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.caminhao
    ).scalar()

    caminhonetes = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.caminhonete
    ).scalar()

    motorizadas = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.motorizada
    ).scalar()

    autocarros = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.autocarro
    ).scalar()

    mini_autocarros = db.query(func.count(Veiculo.id)).filter(
        Veiculo.tipo == TipoVeiculo.mini_autocarro
    ).scalar()

    return {
        "total": total,
        "ativos": activos,
        "inativos": inactivos,

        "tipos": {
            "carros": carros,
            "caminhoes": caminhoes,
            "caminhonetes": caminhonetes,
            "motorizadas": motorizadas,
            "autocarros": autocarros,
            "miniAutocarros": mini_autocarros
        }
    }

#onestate