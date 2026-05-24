from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

from app.schemas.veiculo import VeiculoMiniResponse


# =========================
# ENUM
# =========================
class TipoDespesa(str, Enum):
    combustivel = "combustivel"
    manutencao = "manutencao"
    seguro = "seguro"
    pneu = "pneu"
    lavagem = "lavagem"
    outro = "outro"


# =========================
# BASE
# =========================
class DespesaBase(BaseModel):
    tipo: TipoDespesa
    valor: float
    data: datetime
    descricao: str

    veiculo_id: str

    recibo: Optional[str] = None
    pago: bool = False


# =========================
# CREATE
# =========================
class DespesaCreate(DespesaBase):
    pass


# =========================
# UPDATE (PATCH REAL)
# =========================
class DespesaUpdate(BaseModel):
    tipo: Optional[TipoDespesa] = None
    valor: Optional[float] = None
    data: Optional[datetime] = None
    descricao: Optional[str] = None

    veiculo_id: Optional[str] = None

    recibo: Optional[str] = None
    pago: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE
# =========================
class DespesaResponse(BaseModel):
    id: str

    tipo: TipoDespesa
    valor: float
    data: datetime
    descricao: str

    veiculo_id: str

    recibo: Optional[str] = None
    pago: bool

    veiculo: Optional[VeiculoMiniResponse] = None

    model_config = ConfigDict(from_attributes=True)








# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import datetime
# from app.schemas.veiculo import VeiculoMiniResponse

# from enum import Enum

# class TipoDespesa(str, Enum):
#     combustivel = 'combustivel'
#     manutencao = 'manutencao'
#     seguro = 'seguro'
#     pneu = 'pneu'
#     lavagem = 'lavagem'
#     outro = 'outro'

# class DespesaBase(BaseModel):
#     tipo: TipoDespesa
#     valor: float
#     data: datetime
#     descricao: str
#     veiculo_id: str 
#     recibo: Optional[str] = None
#     pago: bool = False


# class DespesaCreate(DespesaBase):
#     pass


# class DespesaUpdate(BaseModel):
#     tipo: Optional[TipoDespesa]
#     valor: Optional[float]
#     data: Optional[datetime]
#     descricao: Optional[str]
#     veiculo_id: Optional[str]
#     recibo: Optional[str]
#     pago: Optional[bool]



# class DespesaResponse(BaseModel):
#     id: str
#     tipo: str
#     valor: float
#     data: datetime
#     descricao: str
#     veiculo_id: str
#     recibo: str | None
#     pago: bool

#     veiculo: VeiculoMiniResponse | None = None

#     class Config:
#         from_attributes = True
