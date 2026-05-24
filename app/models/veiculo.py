import uuid
import enum

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Float,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class TipoVeiculo(str, enum.Enum):
    carro = "carro"
    caminhao = "caminhao"
    caminhonete = "caminhonete"
    motorizada = "motorizada"
    autocarro = "autocarro"
    mini_autocarro = "mini_autocarro"


class Combustivel(str, enum.Enum):
    gasolina = "gasolina"
    etanol = "etanol"
    diesel = "diesel"
    eletrico = "eletrico"


class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    placa = Column(
        String(15),
        nullable=False
    )

    modelo = Column(
        String(100),
        nullable=True
    )

    marca = Column(
        String(100),
        nullable=True
    )

    ano = Column(
        Integer,
        nullable=True
    )

    vin = Column(
        String(50),
        nullable=True
    )

    tipo = Column(
        Enum(TipoVeiculo),
        nullable=True
    )

    capacidade_carga = Column(
        Float,
        nullable=True
    )

    combustivel = Column(
        Enum(Combustivel),
        nullable=True
    )

    consumo_medio = Column(
        Float,
        nullable=True
    )

    ultima_revisao = Column(
        DateTime,
        nullable=True
    )

    data_cadastro = Column(
        DateTime,
        default=datetime.utcnow
    )

    ativo = Column(
        Boolean,
        default=True
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

    # RELACIONAMENTOS

    empresa = relationship(
        "Empresa",
        back_populates="veiculos"
    )

    viagens = relationship(
        "Viagem",
        back_populates="veiculo",
        cascade="all, delete-orphan"
    )

    despesas = relationship(
        "Despesa",
        back_populates="veiculo",
        cascade="all, delete-orphan"
    )

    manutencoes = relationship(
        "ManutencaoVeiculo",
        back_populates="veiculo",
        cascade="all, delete-orphan"
    )

    __table_args__ = (

        UniqueConstraint(
            "empresa_id",
            "placa",
            name="uq_veiculo_empresa_placa"
        ),

        UniqueConstraint(
            "empresa_id",
            "vin",
            name="uq_veiculo_empresa_vin"
        ),
    )




# from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, Enum
# from app.core.database import Base
# import uuid
# import enum
# from datetime import datetime
# from sqlalchemy.orm import relationship


# class TipoVeiculo(str, enum.Enum):
#     carro = "carro"
#     caminhao = "caminhao"
#     caminhonete = "caminhonete"
#     motorizada = "motorizada"
#     autocarro = "autocarro"
#     mini_autocarro = "mini_autocarro"
    
# class Combustivel(str, enum.Enum):
#     gasolina = "gasolina"
#     etanol = "etanol"
#     diesel = "diesel"
#     eletrico = "eletrico"

    
# class Veiculo(Base):
#     __tablename__ = "veiculos"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     placa = Column(String(15), unique=True, nullable=False)
#     modelo = Column(String(100))
#     marca = Column(String(100))
#     ano = Column(Integer)
#     VIN = Column(String(50), unique=True)
#     tipo = Column(Enum(TipoVeiculo))
#     capacidadeCarga = Column(Float)
#     dataCadastro = Column(DateTime)
#     ativo = Column(Boolean, default=True)
#     combustivel = Column(Enum(Combustivel))
#     consumoMedio = Column(Float)
#     ultimaRevista = Column(DateTime)
#     criadoEm = Column(DateTime, default=datetime.utcnow)
    
   
#     viagens = relationship("Viagem", back_populates="veiculo")
#     despesas = relationship("Despesa", back_populates="veiculo")
#     manutencoes = relationship("ManutencaoVeiculo", back_populates="veiculo")
