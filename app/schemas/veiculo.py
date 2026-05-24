from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum



# =========================
# ENUMS
# =========================
class TipoVeiculo(str, Enum):
    carro = "carro"
    caminhao = "caminhao"
    caminhonete = "caminhonete"
    motorizada = "motorizada"
    autocarro = "autocarro"
    mini_autocarro = "mini_autocarro"


class Combustivel(str, Enum):
    gasolina = "gasolina"
    etanol = "etanol"
    diesel = "diesel"
    eletrico = "eletrico"


# =========================
# BASE (INPUT CORE)
# =========================
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    marca: str
    ano: int
    vin: str

    tipo: TipoVeiculo
    combustivel: Combustivel

    capacidade_carga: float
    consumo_medio: float

    ativo: bool = True


# =========================
# CREATE
# =========================
class VeiculoCreate(VeiculoBase):
    vin: str

    model_config = ConfigDict(populate_by_name=True)


# =========================
# UPDATE (SAFE PATCH)
# =========================
class VeiculoUpdate(BaseModel):
    placa: Optional[str] = None
    modelo: Optional[str] = None
    marca: Optional[str] = None
    ano: Optional[int] = None
    vin: Optional[str] = None

    tipo: Optional[TipoVeiculo] = None
    combustivel: Optional[Combustivel] = None

    capacidade_carga: Optional[float] = None
    consumo_medio: Optional[float] = None

    ativo: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# MINI RESPONSE
# =========================
class VeiculoMiniResponse(BaseModel):
    id: str
    placa: str
    marca: str
    modelo: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# FULL RESPONSE
# =========================
class VeiculoResponse(BaseModel):
    id: str

    placa: str
    modelo: str
    marca: str
    ano: int
    vin: str

    tipo: TipoVeiculo
    combustivel: Combustivel

    capacidade_carga: float
    consumo_medio: float
    ativo: bool

    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)












# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
# from enum import Enum
# from pydantic import BaseModel


# class TipoVeiculo(str, Enum):
#     carro = "carro"
#     caminhao = "caminhao"
#     caminhonete = "caminhonete"
#     motorizada = "motorizada"
#     autocarro = "autocarro"
#     mini_autocarro = "mini_autocarro"



# class Combustivel(str, Enum):
#     gasolina = "gasolina"
#     etanol = "etanol"
#     diesel = "diesel"
#     eletrico = "eletrico"

    
# class VeiculoBase(BaseModel):
#     placa: str
#     modelo: str
#     marca: str
#     ano: int
#     VIN: str
#     tipo: TipoVeiculo
#     capacidadeCarga: float
#     dataCadastro: datetime
#     ativo: bool = True
#     combustivel: Combustivel
#     consumoMedio: float
#     ultimaRevista: datetime
    
# class VeiculoCreate(VeiculoBase):
#     pass


# class VeiculoUpdate(BaseModel):
#     placa: Optional[str]
#     modelo: Optional[str]
#     marca: Optional[str]
#     ano: Optional[int]
#     VIN: Optional[str]
#     tipo: Optional[TipoVeiculo]
#     capacidadeCarga: Optional[float]
#     dataCadastro: Optional[datetime]
#     ativo: Optional[bool]
#     combustivel: Optional[Combustivel]
#     consumoMedio: Optional[float]
#     ultimaRevista: Optional[datetime]


# class VeiculoMiniResponse(BaseModel):
#     id: str
#     placa: str
#     marca: str
#     modelo: str

#     class Config:
#         from_attributes = True

# class VeiculoResponse(VeiculoBase):
#     id: str
#     criadoEm: datetime

#     class Config:
#         from_attributes = True
