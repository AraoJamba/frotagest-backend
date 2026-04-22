from pydantic import BaseModel
from enum import Enum


class UnidadeDistancia(str, Enum):
    km = "km"
    mi = "mi"


class UnidadeConsumo(str, Enum):
    kmL = "kmL"
    kmgal = "kmgal"


class UnidadePeso(str, Enum):
    kg = "kg"
    lb = "lb"


class UnidadeTemperatura(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class ConfiguracoesMedidasBase(BaseModel):
    unidade_distancia: UnidadeDistancia
    unidade_consumo_combustivel: UnidadeConsumo
    unidade_peso: UnidadePeso
    unidade_temperatura: UnidadeTemperatura


class ConfiguracoesMedidasCreate(ConfiguracoesMedidasBase):
    pass


class ConfiguracoesMedidasUpdate(ConfiguracoesMedidasBase):
    pass


class ConfiguracoesMedidasResponse(ConfiguracoesMedidasBase):
    id: str

    class Config:
        from_attributes = True
