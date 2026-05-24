from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.despesa import Despesa
from app.models.veiculo import Veiculo
from app.schemas.despesa import DespesaCreate, DespesaUpdate


# =========================
# CREATE (TENANT SAFE)
# =========================
def create_despesa(db: Session, despesa: DespesaCreate, empresa_id: str):

    # validar veículo da empresa
    veiculo = db.query(Veiculo).filter(
        Veiculo.id == despesa.veiculo_id,
        Veiculo.empresa_id == empresa_id
    ).first()

    if not veiculo:
        raise HTTPException(
            status_code=404,
            detail="Veículo inválido para esta empresa"
        )

    data = despesa.dict()
    data["empresa_id"] = empresa_id

    db_despesa = Despesa(**data)

    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)

    return db_despesa


# =========================
# LISTAR (TENANT SAFE)
# =========================
def get_despesas(db: Session, empresa_id: str):
    return db.query(Despesa).filter(
        Despesa.empresa_id == empresa_id
    ).all()


# =========================
# GET BY ID (TENANT SAFE)
# =========================
def get_despesa_by_id(db: Session, despesa_id: str, empresa_id: str):
    return db.query(Despesa).filter(
        Despesa.id == despesa_id,
        Despesa.empresa_id == empresa_id
    ).first()


# =========================
# UPDATE (TENANT SAFE)
# =========================
def update_despesa(
    db: Session,
    despesa_id: str,
    despesa: DespesaUpdate,
    empresa_id: str
):
    db_despesa = get_despesa_by_id(db, despesa_id, empresa_id)

    if not db_despesa:
        return None

    update_data = despesa.dict(exclude_unset=True)

    # normalizar nomes (caso frontend mande camelCase)
    if "veiculoId" in update_data:
        update_data["veiculo_id"] = update_data.pop("veiculoId")

    # validar novo veículo se for alterado
    if "veiculo_id" in update_data:
        veiculo = db.query(Veiculo).filter(
            Veiculo.id == update_data["veiculo_id"],
            Veiculo.empresa_id == empresa_id
        ).first()

        if not veiculo:
            raise HTTPException(
                status_code=400,
                detail="Veículo inválido para esta empresa"
            )

    for key, value in update_data.items():
        setattr(db_despesa, key, value)

    db.commit()
    db.refresh(db_despesa)

    return db_despesa


# =========================
# DELETE (TENANT SAFE)
# =========================
def delete_despesa(db: Session, despesa_id: str, empresa_id: str):
    db_despesa = get_despesa_by_id(db, despesa_id, empresa_id)

    if not db_despesa:
        return None

    db.delete(db_despesa)
    db.commit()

    return db_despesa









# from sqlalchemy.orm import Session
# from app.models.despesa import Despesa
# from app.schemas.despesa import DespesaCreate, DespesaUpdate
# from app.models.veiculo import Veiculo
# from fastapi import HTTPException



# def create_despesa(db: Session, despesa: DespesaCreate):
    
#     veiculo = db.query(Veiculo).filter(
#         Veiculo.id == despesa.veiculo_id
#     ).first()

#     if not veiculo:
#         raise HTTPException(
#             status_code=404,
#             detail="Veículo não encontrado"
#         )

#     db_despesa = Despesa(**despesa.dict())
#     db.add(db_despesa)
#     db.commit()
#     db.refresh(db_despesa)

#     return db_despesa


# def get_despesas(db: Session):
#     return db.query(Despesa).all()


# def get_despesa_by_id(db: Session, despesa_id: str):
#     return db.query(Despesa).filter(Despesa.id == despesa_id).first()


# def update_despesa(db: Session, despesa_id: str, despesa: DespesaUpdate):
#     db_despesa = get_despesa_by_id(db, despesa_id)





#     if not db_despesa:
#         return None

#     update_data = despesa.dict(exclude_unset=True)

#     if "veiculoId" in update_data:
#         update_data["veiculo_id"] = update_data.pop("veiculoId")

#     for key, value in update_data.items():
#         setattr(db_despesa, key, value)

#     db.commit()
#     db.refresh(db_despesa)
#     return db_despesa


# def delete_despesa(db: Session, despesa_id: str):
#     db_despesa = get_despesa_by_id(db, despesa_id)

#     if not db_despesa:
#         return None

#     db.delete(db_despesa)
#     db.commit()
#     return db_despesa
