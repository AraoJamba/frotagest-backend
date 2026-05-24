import uuid
import enum

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class StatusViagem(str, enum.Enum):
    planejada = "planejada"
    em_andamento = "em_andamento"
    concluida = "concluida"
    cancelada = "cancelada"


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    data_inicio = Column(
        DateTime,
        nullable=False
    )

    data_fim = Column(
        DateTime,
        nullable=True
    )

    local_partida = Column(
        String(255),
        nullable=False
    )

    local_destino = Column(
        String(255),
        nullable=False
    )

    distancia = Column(
        Float,
        nullable=True
    )

    quilometragem_inicial = Column(
        Float,
        nullable=True
    )

    quilometragem_final = Column(
        Float,
        nullable=True
    )

    status = Column(
        Enum(StatusViagem),
        nullable=False,
        default=StatusViagem.planejada
    )

    combustivel_gasto = Column(
        Float,
        default=0
    )

    custo_viagem = Column(
        Float,
        default=0
    )

    observacoes = Column(
        String(500),
        nullable=True
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    empresa_id = Column(
        String(36),
        ForeignKey("empresas.id"),
        nullable=False
    )

    motorista_id = Column(
        String(36),
        ForeignKey("motoristas.id"),
        nullable=False
    )

    veiculo_id = Column(
        String(36),
        ForeignKey("veiculos.id"),
        nullable=False
    )

    # RELACIONAMENTOS

    empresa = relationship(
        "Empresa",
        back_populates="viagens"
    )

    motorista = relationship(
        "Motorista",
        back_populates="viagens"
    )

    veiculo = relationship(
        "Veiculo",
        back_populates="viagens"
    )






# import uuid
# from sqlalchemy import Column, String, Float, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from app.core.database import Base


# class Viagem(Base):
#     __tablename__ = "viagens"

#     id = Column(String(50), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

#     data_inicio = Column(DateTime)
#     data_fim = Column(DateTime, nullable=True)

#     local_partida = Column(String(255))
#     local_destino = Column(String(255))

#     distancia = Column(Float)
    
#     status = Column(String(20))

#     combustivel_gasto = Column(Float)
#     custo_viagem = Column(Float)

#     observacoes = Column(String(500), nullable=True)

    
#     # RELACIONAMENTOS
#     motorista_id = Column(String(36), ForeignKey("motoristas.id"))
#     veiculo_id = Column(String(36), ForeignKey("veiculos.id"))

#     motorista = relationship("Motorista", back_populates="viagens")
#     veiculo = relationship("Veiculo", back_populates="viagens")