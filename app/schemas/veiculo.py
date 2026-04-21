from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TipoVeiculo(str, Enum):
    leve = "leve"
    medio = "medio"
    pesado = "pesado"


class Combustivel(str, Enum):
    gasolina = "gasolina"
    diesel = "diesel"
    etanol = "etanol"
    
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    marca: str
    ano: int
    VIN: str
    tipo: TipoVeiculo
    capacidadeCarga: float
    dataCadastro: datetime
    ativo: bool = True
    combustivel: Combustivel
    consumoMedio: float
    ultimaRevista: datetime
    
class VeiculoCreate(VeiculoBase):
    pass


class VeiculoUpdate(BaseModel):
    placa: Optional[str]
    modelo: Optional[str]
    marca: Optional[str]
    ano: Optional[int]
    VIN: Optional[str]
    tipo: Optional[TipoVeiculo]
    capacidadeCarga: Optional[float]
    dataCadastro: Optional[datetime]
    ativo: Optional[bool]
    combustivel: Optional[Combustivel]
    consumoMedio: Optional[float]
    ultimaRevista: Optional[datetime]

class VeiculoResponse(VeiculoBase):
    id: str
    criadoEm: datetime

    class Config:
        from_attributes = True
