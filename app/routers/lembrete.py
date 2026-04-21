from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.lembrete import (
    LembreteCreate,
    LembreteUpdate,
    LembreteResponse
)

from app.crud import lembrete as lembrete_crud

router = APIRouter(
    prefix="/lembretes",
    tags=["Lembretes"]
)


@router.post("/", response_model=LembreteResponse)
def criar(lembrete: LembreteCreate, db: Session = Depends(get_db)):
    return lembrete_crud.create_lembrete(db, lembrete)


@router.get("/", response_model=list[LembreteResponse])
def listar(db: Session = Depends(get_db)):
    return lembrete_crud.get_lembretes(db)


@router.get("/{lembrete_id}", response_model=LembreteResponse)
def pegar_por_id(lembrete_id: str, db: Session = Depends(get_db)):
    lembrete = lembrete_crud.get_lembrete_by_id(db, lembrete_id)

    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return lembrete


@router.put("/{lembrete_id}", response_model=LembreteResponse)
def atualizar(
    lembrete_id: str,
    lembrete: LembreteUpdate,
    db: Session = Depends(get_db)
):
    lembrete_atualizado = lembrete_crud.update_lembrete(
        db,
        lembrete_id,
        lembrete
    )

    if not lembrete_atualizado:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return lembrete_atualizado


@router.delete("/{lembrete_id}")
def deletar(lembrete_id: str, db: Session = Depends(get_db)):
    lembrete = lembrete_crud.delete_lembrete(db, lembrete_id)

    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return {"message": "Lembrete deletado com sucesso"}
