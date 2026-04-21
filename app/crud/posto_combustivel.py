from sqlalchemy.orm import Session
from app.models.posto_combustivel import PostoCombustivel
from app.schemas.posto_combustivel import (
    PostoCombustivelCreate,
    PostoCombustivelUpdate
)


def create_posto(db: Session, posto: PostoCombustivelCreate):
    db_posto = PostoCombustivel(**posto.dict())
    db.add(db_posto)
    db.commit()
    db.refresh(db_posto)
    return db_posto


def get_postos(db: Session):
    return db.query(PostoCombustivel).all()


def get_posto_by_id(db: Session, posto_id: str):
    return db.query(PostoCombustivel).filter(
        PostoCombustivel.id == posto_id
    ).first()


def update_posto(db: Session, posto_id: str, posto: PostoCombustivelUpdate):
    db_posto = get_posto_by_id(db, posto_id)

    if not db_posto:
        return None

    for key, value in posto.dict().items():
        setattr(db_posto, key, value)

    db.commit()
    db.refresh(db_posto)

    return db_posto


def delete_posto(db: Session, posto_id: str):
    db_posto = get_posto_by_id(db, posto_id)

    if not db_posto:
        return None

    db.delete(db_posto)
    db.commit()

    return db_posto
