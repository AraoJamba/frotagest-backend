from sqlalchemy.orm import Session
from app.models.servico import Servico
from app.schemas.servico import ServicoCreate, ServicoUpdate


def create_servico(db: Session, servico: ServicoCreate):
    db_servico = Servico(**servico.dict())
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico


def get_servicos(db: Session):
    return db.query(Servico).all()


def get_servico_by_id(db: Session, servico_id: str):
    return db.query(Servico).filter(
        Servico.id == servico_id
    ).first()


def update_servico(
    db: Session,
    servico_id: str,
    servico: ServicoUpdate
):
    db_servico = get_servico_by_id(db, servico_id)

    if db_servico:
        for key, value in servico.dict().items():
            setattr(db_servico, key, value)

        db.commit()
        db.refresh(db_servico)

    return db_servico


def delete_servico(db: Session, servico_id: str):
    db_servico = get_servico_by_id(db, servico_id)

    if db_servico:
        db.delete(db_servico)
        db.commit()

    return db_servico
