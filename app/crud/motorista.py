from sqlalchemy.orm import Session
from app.models.motorista import Motorista
from app.schemas.motorista import MotoristaCreate, MotoristaUpdate


def create_motorista(db: Session, motorista: MotoristaCreate):
    db_motorista = Motorista(**motorista.dict())
    db.add(db_motorista)
    db.commit()
    db.refresh(db_motorista)
    return db_motorista


def get_motoristas(db: Session):
    return db.query(Motorista).all()


def get_motorista_by_id(db: Session, motorista_id: str):
    return db.query(Motorista).filter(Motorista.id == motorista_id).first()


def update_motorista(db: Session, motorista_id: str, motorista: MotoristaUpdate):
    db_motorista = get_motorista_by_id(db, motorista_id)

    if not db_motorista:
        return None

    for key, value in motorista.dict().items():
        setattr(db_motorista, key, value)

    db.commit()
    db.refresh(db_motorista)

    return db_motorista


def delete_motorista(db: Session, motorista_id: str):
    db_motorista = get_motorista_by_id(db, motorista_id)

    if not db_motorista:
        return None

    db.delete(db_motorista)
    db.commit()

    return db_motorista