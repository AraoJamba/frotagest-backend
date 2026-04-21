from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.despesa import DespesaCreate, DespesaUpdate, DespesaResponse
from app.crud.despesa import create_despesa, delete_despesa, get_despesas, get_despesa_by_id, update_despesa

router = APIRouter(prefix="/despesas", tags=["Despesas"])


@router.post("/", response_model=DespesaResponse)
def criar(despesa: DespesaCreate, db: Session = Depends(get_db)):
    return create_despesa(db, despesa)


@router.get("/", response_model=list[DespesaResponse])
def listar(db: Session = Depends(get_db)):
    return get_despesas(db)


@router.get("/{despesa_id}", response_model=DespesaResponse)
def buscar(despesa_id: str, db: Session = Depends(get_db)):
    despesa = get_despesa_by_id(db, despesa_id)

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return despesa


@router.put("/{despesa_id}", response_model=DespesaResponse)
def atualizar(despesa_id: str, despesa: DespesaUpdate, db: Session = Depends(get_db)):
    despesa_atualizada = update_despesa(db, despesa_id, despesa)

    if not despesa_atualizada:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return despesa_atualizada


@router.delete("/{despesa_id}")
def deletar(despesa_id: str, db: Session = Depends(get_db)):
    despesa = delete_despesa(db, despesa_id)

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return {"message": "Despesa deletada com sucesso"}
