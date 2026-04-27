import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TipoManutencao(str, enum.Enum):
    preventiva = "preventiva"
    corretiva = "corretiva"
    manutencao = "manutencao"
    reparo = "reparo"
    inspecao = "inspecao"


class StatusManutencao(str, enum.Enum):
    agendada = "agendada"
    emAndamento = "emAndamento"
    concluida = "concluida"
    cancelada = "cancelada"


class ManutencaoVeiculo(Base):
    __tablename__ = "manutencoes_veiculo"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    veiculo_id = Column(
        String(36),
        ForeignKey("veiculos.id"),
        nullable=False
    )

    tipo_manutencao = Column(
        Enum(TipoManutencao),
        nullable=False
    )

    descricao = Column(String(255), nullable=False)

    data_agendada = Column(DateTime, nullable=False)

    data_conclusao = Column(DateTime, nullable=True)

    responsavel = Column(String(100), nullable=False)

    custo = Column(Float, nullable=False)

    status = Column(
        Enum(StatusManutencao),
        default=StatusManutencao.agendada
    )

    criado_em = Column(DateTime, server_default=func.now())
