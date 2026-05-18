from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.veiculo import VeiculoMiniResponse

from enum import Enum

class TipoDespesa(str, Enum):
    combustivel = 'combustivel'
    manutencao = 'manutencao'
    seguro = 'seguro'
    pneu = 'pneu'
    lavagem = 'lavagem'
    outro = 'outro'

class DespesaBase(BaseModel):
    tipo: TipoDespesa
    valor: float
    data: datetime
    descricao: str
    veiculo_id: str 
    recibo: Optional[str] = None
    pago: bool = False


class DespesaCreate(DespesaBase):
    pass


class DespesaUpdate(BaseModel):
    tipo: Optional[TipoDespesa]
    valor: Optional[float]
    data: Optional[datetime]
    descricao: Optional[str]
    veiculo_id: Optional[str]
    recibo: Optional[str]
    pago: Optional[bool]



class DespesaResponse(BaseModel):
    id: str
    tipo: str
    valor: float
    data: datetime
    descricao: str
    veiculo_id: str
    recibo: str | None
    pago: bool

    veiculo: VeiculoMiniResponse | None = None

    class Config:
        from_attributes = True
