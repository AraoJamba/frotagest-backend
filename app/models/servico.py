import uuid
import enum
from sqlalchemy import Column, String, Float, Boolean, DateTime, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func

from app.core.database import Base


class TipoServico(str, enum.Enum):
    manutencao = "manutencao"
    reparo = "reparo"
    inspecao = "inspecao"


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    nome = Column(String(100), nullable=False)

    descricao = Column(String(255), nullable=False)

    tipo = Column(
        Enum(TipoServico),
        nullable=False
    )

    custo_estimado = Column(Float, nullable=False)

    data_cadastro = Column(
        DateTime,
        server_default=func.now()
    )

    ativo = Column(Boolean, default=True)
