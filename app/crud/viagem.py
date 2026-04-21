from sqlalchemy.orm import Session
from app.models.viagem import Viagem
from app.schemas.viagem import ViagemCreate, ViagemUpdate


def create_viagem(db: Session, viagem: ViagemCreate):
    db_viagem = Viagem(**viagem.dict())
    db.add(db_viagem)
    db.commit()
    db.refresh(db_viagem)
    return db_viagem


def get_viagens(db: Session):
    return db.query(Viagem).all()


def get_viagem_by_id(db: Session, viagem_id: str):
    return db.query(Viagem).filter(Viagem.id == viagem_id).first()


def update_viagem(db: Session, viagem_id: str, viagem: ViagemUpdate):
    db_viagem = get_viagem_by_id(db, viagem_id)

    if not db_viagem:
        return None

    for key, value in viagem.dict(exclude_unset=True).items():
        setattr(db_viagem, key, value)

    db.commit()
    db.refresh(db_viagem)

    return db_viagem


def delete_viagem(db: Session, viagem_id: str):
    db_viagem = get_viagem_by_id(db, viagem_id)

    if not db_viagem:
        return None

    db.delete(db_viagem)
    db.commit()

    return db_viagem