from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.schemas.manutencao_veiculo import (
    ManutencaoCreate,
    ManutencaoUpdate,
    ManutencaoResponse
)

from app.crud import manutencao_veiculo as crud

from sqlalchemy import func
from app.models.manutencao_veiculo import ManutencaoVeiculo, TipoManutencao, StatusManutencao


router = APIRouter(prefix="/manutencoes", tags=["Manutencoes"])


@router.post("/", response_model=ManutencaoResponse)
def criar(manutencao: ManutencaoCreate, db: Session = Depends(get_db)):
    return crud.create_manutencao(db, manutencao)


@router.get("/", response_model=list[ManutencaoResponse])
def listar(db: Session = Depends(get_db)):
    manutencoes = db.query(ManutencaoVeiculo).options(
        selectinload(ManutencaoVeiculo.veiculo)
    ).all()

    return manutencoes



@router.get("/{manutencao_id}", response_model=ManutencaoResponse)
def pegar_por_id(manutencao_id: str, db: Session = Depends(get_db)):
    manutencao = db.query(ManutencaoVeiculo).options(
        selectinload(ManutencaoVeiculo.veiculo)
    ).filter(
        ManutencaoVeiculo.id == manutencao_id
    ).first()

    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    return manutencao


@router.put("/{manutencao_id}", response_model=ManutencaoResponse)
def atualizar(
    manutencao_id: str,
    manutencao: ManutencaoUpdate,
    db: Session = Depends(get_db)
):
    manutencao_db = crud.update_manutencao(
        db,
        manutencao_id,
        manutencao
    )

    if not manutencao_db:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    return manutencao_db


@router.delete("/{manutencao_id}")
def deletar(manutencao_id: str, db: Session = Depends(get_db)):
    manutencao = crud.delete_manutencao(db, manutencao_id)

    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    return {"message": "Manutenção deletada com sucesso"}



@router.get("/veiculo/{veiculo_id}", response_model=list[ManutencaoResponse])
def manutencoes_por_veiculo(
    veiculo_id: str,
    db: Session = Depends(get_db)
):
    manutencoes = db.query(ManutencaoVeiculo).options(
        selectinload(ManutencaoVeiculo.veiculo)
    ).filter(
        ManutencaoVeiculo.veiculo_id == veiculo_id
    ).all()

    return manutencoes



@router.get("/estatisticas/resumo")
def resumo_veiculos(db: Session = Depends(get_db)):

    total = db.query(func.count(ManutencaoVeiculo.id)).scalar()


    #tipos
    corretiva = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.tipo_manutencao == TipoManutencao.corretiva
    ).scalar()

    inspecao = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.tipo_manutencao == TipoManutencao.inspecao
    ).scalar()

    manutencao = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.tipo_manutencao == TipoManutencao.manutencao
    ).scalar()

    preventiva = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.tipo_manutencao == TipoManutencao.preventiva
    ).scalar()

    reparo = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.tipo_manutencao == TipoManutencao.reparo
    ).scalar()

    # status
    agendada = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.status == StatusManutencao.agendada
    ).scalar()

    cancelada = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.status == StatusManutencao.cancelada
    ).scalar()

    concluida = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.status == StatusManutencao.concluida
    ).scalar()

    emAndamento = db.query(func.count(ManutencaoVeiculo.id)).filter(
        ManutencaoVeiculo.status == StatusManutencao.emAndamento
    ).scalar()

    return {
        "total": total,
        "status": {
            "agendadas": agendada,
            "concluidas": concluida,
            "cancelada": cancelada,
            "emAndamento": emAndamento
        },

        "tipos": {
            "corretiva": corretiva,
            "caminhoes": inspecao,
            "preventiva": preventiva,
            "manutencao": manutencao,
            "reparo": reparo
        }
    }

#onestate
