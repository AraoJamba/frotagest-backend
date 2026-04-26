from sqlalchemy.orm import Session, joinedload
from app.models.viagem import Viagem
from app.models.motorista import Motorista
from app.models.veiculo import Veiculo
from app.schemas.viagem import ViagemCreate, ViagemUpdate
from app.models.viagem import Viagem
from sqlalchemy import or_, cast, String
from typing import Optional
from sqlalchemy.orm import selectinload


def get_viagem_by_id(db: Session, viagem_id: str):
    return db.query(Viagem).options(
        joinedload(Viagem.motorista), 
        joinedload(Viagem.veiculo)
    ).filter(Viagem.id == viagem_id).first()





# def get_viagem_by_id(db: Session, viagem_id: str):
#     viagem = (
#         db.query(Viagem)
#         .join(Motorista, Viagem.motorista_id == Motorista.id)
#         .join(Veiculo, Viagem.veiculo_id == Veiculo.id)
#         .filter(Viagem.id == viagem_id)
#         .first()
#     )

#     if not viagem:
#         return None

#     return {
#         **viagem.__dict__,
#         "motorista": viagem.motorista,
#         "veiculo": viagem.veiculo
#     }


def create_viagem(db: Session, viagem: ViagemCreate):
    db_viagem = Viagem(**viagem.dict())
    db.add(db_viagem)
    db.commit()
    db.refresh(db_viagem)
    return db_viagem


def get_viagens(
    db: Session,
    search: Optional[str] = None,
    data_inicio: Optional[str] = None,
    local_partida: Optional[str] = None,
    local_destino: Optional[str] = None,
    status: Optional[str] = None
):
    query = db.query(Viagem).options(
        joinedload(Viagem.motorista),
        joinedload(Viagem.veiculo)
    )

    if search:
        query = query.filter(
            Viagem.local_partida.contains(search) |
            Viagem.local_destino.contains(search) |
            Viagem.status.contains(search)
        )

    if data_inicio:
        query = query.filter(Viagem.data_inicio.cast(String).contains(data_inicio))

    if local_partida:
        query = query.filter(Viagem.local_partida.contains(local_partida))

    if local_destino:
        query = query.filter(Viagem.local_destino.contains(local_destino))

    if status:
        query = query.filter(Viagem.status == status)

    return query.all()



# def get_viagens(
#     db,
#     search: Optional[str] = None,
#     data_inicio: Optional[str] = None,
#     local_partida: Optional[str] = None,
#     local_destino: Optional[str] = None,
#     status: Optional[str] = None
# ):
#     query = db.query(Viagem)

#     if search:
#         query = query.filter(
#             or_(
#                 Viagem.local_partida.contains(search),
#                 Viagem.data_inicio.contains(search),
#                 Viagem.data_fim.contains(search),
#                 Viagem.local_destino.contains(search),
#                 Viagem.status.contains(search),
#                 cast(Viagem.data_inicio, String).contains(search)  # 👈 aqui
#             )
#         )

#     if data_inicio:
#         query = query.filter(cast(Viagem.data_inicio, String).contains(data_inicio))

#     if local_partida:
#         query = query.filter(Viagem.local_partida.contains(local_partida))

#     if local_destino:
#         query = query.filter(Viagem.local_destino.contains(local_destino))

#     if status:
#         query = query.filter(Viagem.status == status)

#     return query.all()



def get_viagem_by_id(db: Session, viagem_id: str):
    return (
        db.query(Viagem)
        .join(Motorista, Viagem.motorista_id == Motorista.id)
        .join(Veiculo, Viagem.veiculo_id == Veiculo.id)
        .filter(Viagem.id == viagem_id)
        .first()
    )


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