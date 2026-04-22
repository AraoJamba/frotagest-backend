from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DespesaBase(BaseModel):
    tipo: str
    valor: float
    data: datetime
    descricao: str
    veiculo_id: str 
    recibo: Optional[str] = None
    pago: bool = False


class DespesaCreate(DespesaBase):
    pass


class DespesaUpdate(BaseModel):
    tipo: Optional[str]
    valor: Optional[float]
    data: Optional[datetime]
    descricao: Optional[str]
    veiculo_id: Optional[str]
    recibo: Optional[str]
    pago: Optional[bool]


class DespesaResponse(DespesaBase):
    id: str

    class Config:
        from_attributes = True
