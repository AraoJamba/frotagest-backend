import uuid
import enum

from sqlalchemy import Column, Enum
from sqlalchemy.dialects.mysql import CHAR

from app.core.database import Base


class UnidadeDistancia(str, enum.Enum):
    km = "km"
    mi = "mi"


class UnidadeConsumo(str, enum.Enum):
    kmL = "kmL"
    kmgal = "kmgal"


class UnidadePeso(str, enum.Enum):
    kg = "kg"
    lb = "lb"


class UnidadeTemperatura(str, enum.Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class ConfiguracoesMedidas(Base):
    __tablename__ = "configuracoes_medidas"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    unidade_distancia = Column(
        Enum(UnidadeDistancia),
        default=UnidadeDistancia.km
    )

    unidade_consumo_combustivel = Column(
        Enum(UnidadeConsumo),
        default=UnidadeConsumo.kmL
    )

    unidade_peso = Column(
        Enum(UnidadePeso),
        default=UnidadePeso.kg
    )

    unidade_temperatura = Column(
        Enum(UnidadeTemperatura),
        default=UnidadeTemperatura.celsius
    )
