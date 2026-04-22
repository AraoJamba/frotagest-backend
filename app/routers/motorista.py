from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.motorista import (
    MotoristaCreate,
    MotoristaUpdate,
    MotoristaResponse
)

from app.crud.motorista import (
    create_motorista,
    get_motoristas,
    get_motorista_by_id,
    update_motorista,
    delete_motorista
)

from app.core.database import get_db

router = APIRouter(
    prefix="/motoristas",
    tags=["Motoristas"]
)


@router.post("/", response_model=MotoristaResponse)
def create(motorista: MotoristaCreate, db: Session = Depends(get_db)):
    return create_motorista(db, motorista)


from typing import Optional

@router.get("/", response_model=list[MotoristaResponse])
def listar(
    search: Optional[str] = None,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    numero_carta: Optional[str] = None,
    numero_bi: Optional[str] = None,
    categoria_carta: Optional[str] = None,
    provincia: Optional[str] = None,
    data_nascimento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_motoristas(
        db,
        search,
        email,
        telefone,
        numero_carta,
        numero_bi,
        categoria_carta,
        provincia,
        data_nascimento
    )



@router.get("/{motorista_id}", response_model=MotoristaResponse)
def get_by_id(motorista_id: str, db: Session = Depends(get_db)):
    motorista = get_motorista_by_id(db, motorista_id)
    
    if not motorista:
        raise HTTPException(404, "Motorista não encontrado")

    return motorista

@router.put("/{motorista_id}", response_model=MotoristaResponse)
def update(
    motorista_id: str,
    motorista: MotoristaUpdate,
    db: Session = Depends(get_db)
):
    motorista_updated = update_motorista(db, motorista_id, motorista)

    if not motorista_updated:
        raise HTTPException(404, "Motorista não encontrado")

    return motorista_updated

@router.delete("/{motorista_id}")
def delete(motorista_id: str, db: Session = Depends(get_db)):
    motorista_deleted = delete_motorista(db, motorista_id)

    if not motorista_deleted:
        raise HTTPException(404, "Motorista não encontrado")

    return {"message": "Motorista deletado com sucesso"}