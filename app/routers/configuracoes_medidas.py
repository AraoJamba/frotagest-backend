from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.configuracoes_medidas import (
    ConfiguracoesMedidasCreate,
    ConfiguracoesMedidasUpdate,
    ConfiguracoesMedidasResponse
)

from app.crud import configuracoes_medidas as crud


router = APIRouter(
    prefix="/configuracoes-medidas",
    tags=["Configurações Medidas"]
)


@router.post("/", response_model=ConfiguracoesMedidasResponse)
def criar(config: ConfiguracoesMedidasCreate, db: Session = Depends(get_db)):
    return crud.create_configuracoes(db, config)


@router.get("/", response_model=list[ConfiguracoesMedidasResponse])
def listar(db: Session = Depends(get_db)):
    return crud.get_configuracoes(db)


@router.get("/{config_id}", response_model=ConfiguracoesMedidasResponse)
def pegar_por_id(config_id: str, db: Session = Depends(get_db)):
    config = crud.get_configuracao_by_id(db, config_id)

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada"
        )

    return config


@router.put("/{config_id}", response_model=ConfiguracoesMedidasResponse)
def atualizar(
    config_id: str,
    config: ConfiguracoesMedidasUpdate,
    db: Session = Depends(get_db)
):
    config_db = crud.update_configuracao(
        db,
        config_id,
        config
    )

    if not config_db:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada"
        )

    return config_db


@router.delete("/{config_id}")
def deletar(config_id: str, db: Session = Depends(get_db)):
    config = crud.delete_configuracao(db, config_id)

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada"
        )

    return {"message": "Configuração deletada com sucesso"}
