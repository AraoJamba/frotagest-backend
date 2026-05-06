from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.lembrete import Lembrete, TipoLembrete, PrioridadeLembrete
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


@router.get("/estatisticas/resumo")
def resumo_veiculos(db: Session = Depends(get_db)):

    total = db.query(func.count(Lembrete.id)).scalar()

    completado = db.query(func.count(Lembrete.id)).filter(
        Lembrete.completado == True
    ).scalar()

    nao_completado = db.query(func.count(Lembrete.id)).filter(
        Lembrete.completado == False
    ).scalar()

    #tipo
    documentacao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.tipo == TipoLembrete.documentacao
    ).scalar()

    manutencao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.tipo == TipoLembrete.manutencao
    ).scalar()

    revisao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.tipo == TipoLembrete.revisao
    ).scalar()

    outro = db.query(func.count(Lembrete.id)).filter(
        Lembrete.tipo == TipoLembrete.outro
    ).scalar()

    #prioridade
    alta = db.query(func.count(Lembrete.id)).filter(
        Lembrete.prioridade == PrioridadeLembrete.alta
    ).scalar()

    media = db.query(func.count(Lembrete.id)).filter(
        Lembrete.prioridade == PrioridadeLembrete.media
    ).scalar()

    baixa = db.query(func.count(Lembrete.id)).filter(
        Lembrete.prioridade == PrioridadeLembrete.baixa
    ).scalar()


    return {
        "total": total,
        "completados": completado,
        "nao_completado": nao_completado,

        "prioridade": {
            "alta": alta,
            "baixa": baixa,
            "media": media
        },
 
        "tipos": {
            "documentacao": documentacao,
            "revisoes": revisao,
            "manutencoes": manutencao,
            "outros": outro
        }
    }
