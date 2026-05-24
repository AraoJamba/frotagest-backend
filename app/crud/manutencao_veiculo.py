from sqlalchemy.orm import Session
from typing import Optional

from app.models.manutencao_veiculo import ManutencaoVeiculo
from app.models.veiculo import Veiculo
from app.schemas.manutencao_veiculo import (
    ManutencaoCreate,
    ManutencaoUpdate
)


# =========================
# CREATE (TENANT SAFE)
# =========================
def create_manutencao(db: Session, manutencao: ManutencaoCreate, empresa_id: str):

    # validar veículo da empresa
    veiculo = db.query(Veiculo).filter(
        Veiculo.id == manutencao.veiculo_id,
        Veiculo.empresa_id == empresa_id
    ).first()

    if not veiculo:
        raise Exception("Veículo inválido para esta empresa")

    data = manutencao.dict()
    data["empresa_id"] = empresa_id

    db_manutencao = ManutencaoVeiculo(**data)

    db.add(db_manutencao)
    db.commit()
    db.refresh(db_manutencao)

    return db_manutencao


# =========================
# LISTAR (TENANT SAFE)
# =========================
def get_manutencoes(db: Session, empresa_id: str):
    return db.query(ManutencaoVeiculo).filter(
        ManutencaoVeiculo.empresa_id == empresa_id
    ).all()


# =========================
# GET BY ID (TENANT SAFE)
# =========================
def get_manutencao_by_id(db: Session, manutencao_id: str, empresa_id: str):
    return db.query(ManutencaoVeiculo).filter(
        ManutencaoVeiculo.id == manutencao_id,
        ManutencaoVeiculo.empresa_id == empresa_id
    ).first()


# =========================
# UPDATE (TENANT SAFE)
# =========================
def update_manutencao(
    db: Session,
    manutencao_id: str,
    manutencao: ManutencaoUpdate,
    empresa_id: str
):
    db_manutencao = get_manutencao_by_id(db, manutencao_id, empresa_id)

    if not db_manutencao:
        return None

    for key, value in manutencao.dict(exclude_unset=True).items():
        setattr(db_manutencao, key, value)

    db.commit()
    db.refresh(db_manutencao)

    return db_manutencao


# =========================
# DELETE (TENANT SAFE)
# =========================
def delete_manutencao(db: Session, manutencao_id: str, empresa_id: str):
    db_manutencao = get_manutencao_by_id(db, manutencao_id, empresa_id)

    if not db_manutencao:
        return None

    db.delete(db_manutencao)
    db.commit()

    return db_manutencao








# from sqlalchemy.orm import Session
# from app.models.manutencao_veiculo import ManutencaoVeiculo
# from app.schemas.manutencao_veiculo import (
#     ManutencaoCreate,
#     ManutencaoUpdate
# )


# def create_manutencao(db: Session, manutencao: ManutencaoCreate):
#     db_manutencao = ManutencaoVeiculo(**manutencao.dict())
#     db.add(db_manutencao)
#     db.commit()
#     db.refresh(db_manutencao)
#     return db_manutencao


# def get_manutencoes(db: Session):
#     return db.query(ManutencaoVeiculo).all()


# def get_manutencao_by_id(db: Session, manutencao_id: str):
#     return db.query(ManutencaoVeiculo).filter(
#         ManutencaoVeiculo.id == manutencao_id
#     ).first()


# def update_manutencao(
#     db: Session,
#     manutencao_id: str,
#     manutencao: ManutencaoUpdate
# ):
#     db_manutencao = get_manutencao_by_id(db, manutencao_id)

#     if db_manutencao:
#         for key, value in manutencao.dict().items():
#             setattr(db_manutencao, key, value)

#         db.commit()
#         db.refresh(db_manutencao)

#     return db_manutencao


# def delete_manutencao(db: Session, manutencao_id: str):
#     db_manutencao = get_manutencao_by_id(db, manutencao_id)

#     if db_manutencao:
#         db.delete(db_manutencao)
#         db.commit()

#     return db_manutencao
