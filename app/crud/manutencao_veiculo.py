from sqlalchemy.orm import Session
from app.models.manutencao_veiculo import ManutencaoVeiculo
from app.schemas.manutencao_veiculo import (
    ManutencaoCreate,
    ManutencaoUpdate
)


def create_manutencao(db: Session, manutencao: ManutencaoCreate):
    db_manutencao = ManutencaoVeiculo(**manutencao.dict())
    db.add(db_manutencao)
    db.commit()
    db.refresh(db_manutencao)
    return db_manutencao


def get_manutencoes(db: Session):
    return db.query(ManutencaoVeiculo).all()


def get_manutencao_by_id(db: Session, manutencao_id: str):
    return db.query(ManutencaoVeiculo).filter(
        ManutencaoVeiculo.id == manutencao_id
    ).first()


def update_manutencao(
    db: Session,
    manutencao_id: str,
    manutencao: ManutencaoUpdate
):
    db_manutencao = get_manutencao_by_id(db, manutencao_id)

    if db_manutencao:
        for key, value in manutencao.dict().items():
            setattr(db_manutencao, key, value)

        db.commit()
        db.refresh(db_manutencao)

    return db_manutencao


def delete_manutencao(db: Session, manutencao_id: str):
    db_manutencao = get_manutencao_by_id(db, manutencao_id)

    if db_manutencao:
        db.delete(db_manutencao)
        db.commit()

    return db_manutencao
