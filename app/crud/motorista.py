from sqlalchemy.orm import Session
from app.models.motorista import Motorista
from app.schemas.motorista import MotoristaCreate, MotoristaUpdate
from sqlalchemy import or_, cast, String
from typing import Optional


def create_motorista(db: Session, motorista: MotoristaCreate):
    db_motorista = Motorista(**motorista.dict())
    db.add(db_motorista)
    db.commit()
    db.refresh(db_motorista)
    return db_motorista

def get_motoristas(
    db: Session,
    search: Optional[str] = None,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    numero_carta: Optional[str] = None,
    numero_bi: Optional[str] = None,
    categoria_carta: Optional[str] = None,
    provincia: Optional[str] = None,
    data_nascimento: Optional[str] = None
):
    query = db.query(Motorista)

    # Pesquisa geral
    if search:
        query = query.filter(
            or_(
                Motorista.email.contains(search),
                Motorista.telefone.contains(search),
                Motorista.numero_carta.contains(search),
                Motorista.numero_bi.contains(search),
                Motorista.categoria_carta.contains(search),
                Motorista.provincia.contains(search),
                cast(Motorista.data_nascimento, String).contains(search)
            )
        )

    # Filtros específicos
    if email:
        query = query.filter(Motorista.email.contains(email))

    if telefone:
        query = query.filter(Motorista.telefone.contains(telefone))

    if numero_carta:
        query = query.filter(Motorista.numero_carta.contains(numero_carta))

    if numero_bi:
        query = query.filter(Motorista.numero_bi.contains(numero_bi))

    if categoria_carta:
        query = query.filter(Motorista.categoria_carta == categoria_carta)

    if provincia:
        query = query.filter(Motorista.provincia.contains(provincia))

    if data_nascimento:
        query = query.filter(
            cast(Motorista.data_nascimento, String).contains(data_nascimento)
        )

    return query.all()



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