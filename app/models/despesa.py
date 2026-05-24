import uuid
import enum

from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoDespesa(enum.Enum):
    combustivel = "combustivel"
    manutencao = "manutencao"
    seguro = "seguro"
    pneu = "pneu"
    lavagem = "lavagem"
    outro = "outro"


class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    tipo = Column(
        Enum(TipoDespesa, name="tipo_despesa"),
        nullable=False,
        default=TipoDespesa.outro
    )

    valor = Column(Float, nullable=False)

    data = Column(DateTime, nullable=False)

    descricao = Column(String(255), nullable=False)

    recibo = Column(String(255), nullable=True)

    pago = Column(Boolean, default=False)

    veiculo_id = Column(
        String(36),
        ForeignKey("veiculos.id"),
        nullable=False
    )

    empresa_id = Column(
        String(36),
        ForeignKey("empresas.id"),
        nullable=False
    )

    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    veiculo = relationship(
        "Veiculo",
        back_populates="despesas"
    )

    empresa = relationship(
        "Empresa",
        back_populates="despesas"
    )






# import uuid
# from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
# from sqlalchemy.sql import func
# from app.core.database import Base
# from sqlalchemy import Enum 
# import enum
# from sqlalchemy.orm import relationship
# from pydantic import BaseModel


# class TipoDespesa(enum.Enum):
#     combustivel = "combustivel"
#     manutencao = "manutencao"
#     seguro = "seguro"
#     pneu = "pneu"
#     lavagem = "lavagem"
#     outro = "outro"


# class VeiculoMiniResponse(BaseModel):
#     id: str
#     placa: str
#     marca: str
#     modelo: str

#     class Config:
#         from_attributes = True
    

# class Despesa(Base):
#     __tablename__ = "despesas"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
#     tipo = Column(
#         Enum(TipoDespesa, name="tipo_despesa"),
#         nullable=False,
#         default=TipoDespesa.outro
#     )

#     valor = Column(Float, nullable=False)
#     data = Column(DateTime, nullable=False)
#     descricao = Column(String(255), nullable=False)
#     recibo = Column(String(255), nullable=True)
#     pago = Column(Boolean, default=False)

#     empresa_id = Column(String(36), ForeignKey("empresas.id"), nullable=False)

#     empresa = relationship("Empresa")

#     veiculo_id = Column(String(36), ForeignKey("veiculos.id"), nullable=False)

#     criado_em = Column(DateTime(timezone=True), server_default=func.now())

#     veiculo = relationship("Veiculo", back_populates="despesas")

