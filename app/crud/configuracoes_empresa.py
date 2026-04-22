from sqlalchemy.orm import Session
from app.models.configuracoes_empresa import ConfiguracoesEmpresa
from app.schemas.configuracoes_empresa import (
    ConfiguracoesEmpresaCreate,
    ConfiguracoesEmpresaUpdate
)


def create_empresa(db: Session, empresa: ConfiguracoesEmpresaCreate):
    db_empresa = ConfiguracoesEmpresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


def get_empresas(db: Session):
    return db.query(ConfiguracoesEmpresa).all()


def get_empresa_by_id(db: Session, empresa_id: str):
    return db.query(ConfiguracoesEmpresa).filter(
        ConfiguracoesEmpresa.id == empresa_id
    ).first()


def update_empresa(
    db: Session,
    empresa_id: str,
    empresa: ConfiguracoesEmpresaUpdate
):
    db_empresa = get_empresa_by_id(db, empresa_id)

    if db_empresa:
        for key, value in empresa.dict().items():
            setattr(db_empresa, key, value)

        db.commit()
        db.refresh(db_empresa)

    return db_empresa


def delete_empresa(db: Session, empresa_id: str):
    db_empresa = get_empresa_by_id(db, empresa_id)

    if db_empresa:
        db.delete(db_empresa)
        db.commit()

    return db_empresa
