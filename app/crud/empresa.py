from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate


# =========================
# CREATE EMPRESA
# =========================
def create_empresa(db: Session, empresa: EmpresaCreate):

    # evitar duplicação por nome
    existente = db.query(Empresa).filter(
        Empresa.nome == empresa.nome
    ).first()

    if existente:
        raise Exception("Já existe uma empresa com este nome")

    db_empresa = Empresa(**empresa.dict())

    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)

    return db_empresa


# =========================
# LISTAR EMPRESAS
# =========================
def get_empresas(
    db: Session,
    search: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    provincia: Optional[str] = None
):
    query = db.query(Empresa)

    if search:
        query = query.filter(
            or_(
                Empresa.nome.contains(search),
                Empresa.email.contains(search),
                Empresa.nif.contains(search),
                Empresa.provincia.contains(search)
            )
        )

    if nome:
        query = query.filter(Empresa.nome.contains(nome))

    if email:
        query = query.filter(Empresa.email.contains(email))

    if provincia:
        query = query.filter(Empresa.provincia.contains(provincia))

    return query.all()


# =========================
# GET POR ID
# =========================
def get_empresa_by_id(db: Session, empresa_id: str):
    return db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()


# =========================
# UPDATE EMPRESA
# =========================
def update_empresa(
    db: Session,
    empresa_id: str,
    empresa: EmpresaUpdate
):
    db_empresa = get_empresa_by_id(db, empresa_id)

    if not db_empresa:
        return None

    update_data = empresa.dict(exclude_unset=True)

    # evitar duplicação de nome
    if "nome" in update_data:
        existe = db.query(Empresa).filter(
            Empresa.nome == update_data["nome"],
            Empresa.id != empresa_id
        ).first()

        if existe:
            raise Exception("Já existe outra empresa com este nome")

    for key, value in update_data.items():
        setattr(db_empresa, key, value)

    db.commit()
    db.refresh(db_empresa)

    return db_empresa


# =========================
# DELETE EMPRESA
# =========================
def delete_empresa(db: Session, empresa_id: str):
    db_empresa = get_empresa_by_id(db, empresa_id)

    if not db_empresa:
        return None

    db.delete(db_empresa)
    db.commit()

    return db_empresa