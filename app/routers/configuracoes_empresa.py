from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.configuracoes_empresa import (
    ConfiguracoesEmpresaCreate,
    ConfiguracoesEmpresaUpdate,
    ConfiguracoesEmpresaResponse
)

from app.crud import configuracoes_empresa as crud


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


@router.post("/", response_model=ConfiguracoesEmpresaResponse)
def criar(empresa: ConfiguracoesEmpresaCreate, db: Session = Depends(get_db)):
    return crud.create_empresa(db, empresa)


@router.get("/", response_model=list[ConfiguracoesEmpresaResponse])
def listar(db: Session = Depends(get_db)):
    return crud.get_empresas(db)


@router.get("/{empresa_id}", response_model=ConfiguracoesEmpresaResponse)
def pegar_por_id(empresa_id: str, db: Session = Depends(get_db)):
    empresa = crud.get_empresa_by_id(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return empresa


@router.put("/{empresa_id}", response_model=ConfiguracoesEmpresaResponse)
def atualizar(
    empresa_id: str,
    empresa: ConfiguracoesEmpresaUpdate,
    db: Session = Depends(get_db)
):
    empresa_db = crud.update_empresa(
        db,
        empresa_id,
        empresa
    )

    if not empresa_db:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return empresa_db


@router.delete("/{empresa_id}")
def deletar(empresa_id: str, db: Session = Depends(get_db)):
    empresa = crud.delete_empresa(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return {"message": "Empresa deletada com sucesso"}
