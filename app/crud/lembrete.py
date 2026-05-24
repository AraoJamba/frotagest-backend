from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.lembrete import Lembrete
from app.models.veiculo import Veiculo
from app.schemas.lembrete import LembreteCreate, LembreteUpdate


# =========================
# CREATE (TENANT SAFE)
# =========================
def create_lembrete(db: Session, lembrete: LembreteCreate, empresa_id: str):

    # validar veículo pertence à empresa
    if lembrete.veiculo_id:
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == lembrete.veiculo_id,
            Veiculo.empresa_id == empresa_id
        ).first()

        if not veiculo:
            raise HTTPException(status_code=400, detail="Veículo inválido para esta empresa")

    data = lembrete.dict()
    data["empresa_id"] = empresa_id

    db_lembrete = Lembrete(**data)

    db.add(db_lembrete)
    db.commit()
    db.refresh(db_lembrete)

    return db_lembrete


# =========================
# LISTAR (TENANT SAFE)
# =========================
def get_lembretes(db: Session, empresa_id: str):
    return db.query(Lembrete).filter(
        Lembrete.empresa_id == empresa_id
    ).all()


# =========================
# GET BY ID (TENANT SAFE)
# =========================
def get_lembrete_by_id(db: Session, lembrete_id: str, empresa_id: str):
    return db.query(Lembrete).filter(
        Lembrete.id == lembrete_id,
        Lembrete.empresa_id == empresa_id
    ).first()


# =========================
# UPDATE (TENANT SAFE)
# =========================
def update_lembrete(
    db: Session,
    lembrete_id: str,
    lembrete: LembreteUpdate,
    empresa_id: str
):
    db_lembrete = get_lembrete_by_id(db, lembrete_id, empresa_id)

    if not db_lembrete:
        return None

    for key, value in lembrete.dict(exclude_unset=True).items():
        setattr(db_lembrete, key, value)

    db.commit()
    db.refresh(db_lembrete)

    return db_lembrete


# =========================
# DELETE (TENANT SAFE)
# =========================
def delete_lembrete(db: Session, lembrete_id: str, empresa_id: str):
    db_lembrete = get_lembrete_by_id(db, lembrete_id, empresa_id)

    if not db_lembrete:
        return None

    db.delete(db_lembrete)
    db.commit()

    return db_lembrete












# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from app.models.lembrete import Lembrete
# from app.models.veiculo import Veiculo
# from app.schemas.lembrete import LembreteCreate, LembreteUpdate


# def create_lembrete(db: Session, lembrete: LembreteCreate):
    
#     if lembrete.veiculo_id:
#         veiculo = db.query(Veiculo).filter(Veiculo.id == lembrete.veiculo_id).first()
#         if not veiculo:
#             raise HTTPException(status_code=400, detail="Veículo não encontrado")

#     db_lembrete = Lembrete(**lembrete.dict())
#     db.add(db_lembrete)
#     db.commit()
#     db.refresh(db_lembrete)
#     return db_lembrete



# def get_lembretes(db: Session):
#     return db.query(Lembrete).all()


# def get_lembrete_by_id(db: Session, lembrete_id: str):
#     return db.query(Lembrete).filter(
#         Lembrete.id == lembrete_id
#     ).first()


# def update_lembrete(db: Session, lembrete_id: str, lembrete: LembreteUpdate):
#     db_lembrete = get_lembrete_by_id(db, lembrete_id)

#     if not db_lembrete:
#         return None

#     for key, value in lembrete.dict().items():
#         setattr(db_lembrete, key, value)

#     db.commit()
#     db.refresh(db_lembrete)

#     return db_lembrete


# def delete_lembrete(db: Session, lembrete_id: str):
#     db_lembrete = get_lembrete_by_id(db, lembrete_id)

#     if not db_lembrete:
#         return None

#     db.delete(db_lembrete)
#     db.commit()

#     return db_lembrete
