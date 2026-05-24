import uuid
import enum

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoLembrete(enum.Enum):
    manutencao = "manutencao"
    documentacao = "documentacao"
    revisao = "revisao"
    outro = "outro"


class PrioridadeLembrete(enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class Lembrete(Base):
    __tablename__ = "lembretes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    titulo = Column(String(255), nullable=False)

    descricao = Column(String(500), nullable=True)

    tipo = Column(
        Enum(TipoLembrete, name="tipo_lembrete"),
        nullable=False,
        default=TipoLembrete.outro
    )

    prioridade = Column(
        Enum(PrioridadeLembrete, name="prioridade_lembrete"),
        nullable=False,
        default=PrioridadeLembrete.media
    )

    data_agendada = Column(DateTime, nullable=False)

    data_criacao = Column(DateTime, default=datetime.utcnow)

    completado = Column(Boolean, default=False)

    veiculo_id = Column(
        String(36),
        ForeignKey("veiculos.id"),
        nullable=True
    )

    empresa_id = Column(
        String(36),
        ForeignKey("empresas.id"),
        nullable=False
    )

    veiculo = relationship("Veiculo")

    empresa = relationship(
        "Empresa",
        back_populates="lembretes"
    )





# import uuid
# from datetime import datetime
# from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
# from sqlalchemy.orm import relationship
# import enum

# from app.core.database import Base

# class TipoLembrete(enum.Enum):
#     manutencao = 'manutencao'
#     documentacao = 'documentacao'
#     revisao = 'revisao' 
#     outro = 'outro'

# class PrioridadeLembrete(enum.Enum):
#     baixa = 'baixa'  
#     media = 'media' 
#     alta = 'alta'

# class Lembrete(Base):
#     __tablename__ = "lembretes"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

#     titulo = Column(String(255))
#     descricao = Column(String(500))
#     tipo = Column(
#         Enum(TipoLembrete, name="tipo_despesa"),
#         nullable=False,
#         default=TipoLembrete.outro
#     )

#     data_agendada = Column(DateTime)
#     data_criacao = Column(DateTime, default=datetime.utcnow)

#     completado = Column(Boolean, default=False)

#     prioridade = Column(
#         Enum(PrioridadeLembrete, name="tipo_despesa"),
#         nullable=False,
#         default=PrioridadeLembrete.media

#     )

#     empresa_id = Column(String(36), ForeignKey("empresas.id"), nullable=False)

#     empresa = relationship("Empresa")

#     veiculo_id = Column(String(36), ForeignKey("veiculos.id"), nullable=True)
#     motorista_id = Column(String(36), ForeignKey("motoristas.id"), nullable=True)

#     # Relacionamentos
#     veiculo = relationship("Veiculo")
#     motorista = relationship("Motorista")
