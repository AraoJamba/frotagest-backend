from sqlalchemy.orm import Session
from app.models.posto_combustivel import PostoCombustivel

from app.schemas.posto_combustivel import (
    PostoCombustivelCreate,
    PostoCombustivelUpdate
)

from sqlalchemy import or_, cast, String
from typing import Optional

def create_posto(db: Session, posto: PostoCombustivelCreate):
    db_posto = PostoCombustivel(**posto.dict())
    db.add(db_posto)
    db.commit()
    db.refresh(db_posto)
    return db_posto



def get_postos(
    db: Session,
    search: Optional[str] = None,
    nome: Optional[str] = None,
    cidade: Optional[str] = None,
    provincia: Optional[str] = None,
    gasoleo: Optional[str] = None,
    gasolina: Optional[str] = None
):
    query = db.query(PostoCombustivel)

    # Pesquisa geral
    if search:
        query = query.filter(
            or_(
                PostoCombustivel.nome.contains(search),
                PostoCombustivel.cidade.contains(search),
                PostoCombustivel.provincia.contains(search),
                PostoCombustivel.endereco.contains(search),
                cast(PostoCombustivel.gasoleo, String).contains(search),
                cast(PostoCombustivel.gasolina, String).contains(search)
            )
        )

    # Filtros específicos
    if nome:
        query = query.filter(
            PostoCombustivel.nome.contains(nome)
        )

    if cidade:
        query = query.filter(
            PostoCombustivel.cidade.contains(cidade)
        )

    if provincia:
        query = query.filter(
            PostoCombustivel.provincia.contains(provincia)
        )

    if gasoleo:
        query = query.filter(
            cast(PostoCombustivel.gasoleo, String).contains(gasoleo)
        )

    if gasolina:
        query = query.filter(
            cast(PostoCombustivel.gasolina, String).contains(gasolina)
        )

    return query.all()



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
