from sqlalchemy.orm import Session
from app.models.configuracoes_medidas import ConfiguracoesMedidas
from app.schemas.configuracoes_medidas import (
    ConfiguracoesMedidasCreate,
    ConfiguracoesMedidasUpdate
)


def create_configuracoes(db: Session, config: ConfiguracoesMedidasCreate):
    db_config = ConfiguracoesMedidas(**config.dict())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_configuracoes(db: Session):
    return db.query(ConfiguracoesMedidas).all()


def get_configuracao_by_id(db: Session, config_id: str):
    return db.query(ConfiguracoesMedidas).filter(
        ConfiguracoesMedidas.id == config_id
    ).first()


def update_configuracao(
    db: Session,
    config_id: str,
    config: ConfiguracoesMedidasUpdate
):
    db_config = get_configuracao_by_id(db, config_id)

    if db_config:
        for key, value in config.dict().items():
            setattr(db_config, key, value)

        db.commit()
        db.refresh(db_config)

    return db_config


def delete_configuracao(db: Session, config_id: str):
    db_config = get_configuracao_by_id(db, config_id)

    if db_config:
        db.delete(db_config)
        db.commit()

    return db_config
