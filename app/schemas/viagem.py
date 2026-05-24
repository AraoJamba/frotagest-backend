from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

# from app.schemas.veiculo import VeiculoMiniResponse
from app.models.viagem import StatusViagem


# =========================
# ENUM
# =========================
class TipoStatus(str, Enum):
    planejada = "planejada"
    em_andamento = "em_andamento"
    concluida = "concluida"
    cancelada = "cancelada"


# =========================
# MINI SCHEMAS
# =========================
class MotoristaMini(BaseModel):
    id: str
    nome: str
    model_config = ConfigDict(from_attributes=True)


class VeiculoMini(BaseModel):
    id: str
    placa: str
    marca: str
    modelo: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# BASE
# =========================
class ViagemBase(BaseModel):
    data_inicio: datetime
    data_fim: Optional[datetime] = None

    local_partida: str
    local_destino: str

    distancia: float
    status: TipoStatus

    combustivel_gasto: float
    custo_viagem: float

    observacoes: Optional[str] = None


# =========================
# CREATE
# =========================
class ViagemCreate(ViagemBase):
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None


# =========================
# UPDATE
# =========================
class ViagemUpdate(BaseModel):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None

    local_partida: Optional[str] = None
    local_destino: Optional[str] = None

    distancia: Optional[float] = None
    status: Optional[TipoStatus] = None

    combustivel_gasto: Optional[float] = None
    custo_viagem: Optional[float] = None

    observacoes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE SIMPLES
# =========================
class ViagemResponse(BaseModel):
    id: str

    motorista_id: Optional[str]
    veiculo_id: Optional[str]

    data_inicio: datetime
    data_fim: Optional[datetime]

    local_partida: str
    local_destino: str

    distancia: float
    status: StatusViagem

    combustivel_gasto: float
    custo_viagem: float

    observacoes: Optional[str]

    veiculo: Optional[VeiculoMini] = None
    motorista: Optional[MotoristaMini] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE DETALHADO
# =========================
class ViagemDetailResponse(ViagemResponse):
    motorista: Optional[MotoristaMini] = None
    veiculo: Optional[VeiculoMini] = None







# from pydantic import BaseModel, ConfigDict
# from typing import Optional
# from datetime import datetime
# from enum import Enum
# from app.schemas.veiculo import VeiculoMiniResponse

# class TipoStatus (str, Enum):
#     planejada = 'planejada'
#     em_andamento = 'em_andamento'
#     concluida = 'concluida'
#     cancelada = 'cancelada'

# class MotoristaMini(BaseModel):
#     id: Optional[str] = None
#     nome: Optional[str] = None
#     model_config = ConfigDict(from_attributes=True)

# class VeiculoMini(BaseModel):
#     id: Optional[str] = None
#     placa: str
#     marca: str
#     modelo: str
#     model_config = ConfigDict(from_attributes=True)

# # --- Schemas da Viagem ---

# class ViagemBase(BaseModel):
#     data_inicio: datetime
#     data_fim: Optional[datetime] = None
#     local_partida: str
#     local_destino: str
#     distancia: float
#     status: TipoStatus
#     combustivel_gasto: float
#     custo_viagem: float
#     observacoes: Optional[str] = None

# class ViagemCreate(ViagemBase):
#     motorista_id: Optional[str] = None
#     veiculo_id: Optional[str] = None

# class ViagemUpdate(BaseModel):
#     data_inicio: Optional[datetime] = None
#     data_fim: Optional[datetime] = None
#     local_partida: Optional[str] = None
#     local_destino: Optional[str] = None
#     status: Optional[TipoStatus] = None
#     distancia: Optional[float] = None
#     combustivel_gasto: Optional[float] = None
#     custo_viagem: Optional[float] = None
#     observacoes: Optional[str] = None

# # class ViagemResponse(ViagemBase):
# #     id: str
# #     motorista_id: Optional[str] = None
# #     veiculo_id: Optional[str] = None
# #     model_config = ConfigDict(from_attributes=True)

# class ViagemResponse(BaseModel):
#     id: str
#     motorista_id: Optional[str] = None
#     veiculo_id: Optional[str] = None
#     data_inicio: Optional[datetime] = None
#     data_fim: Optional[datetime] = None
#     local_partida: Optional[str] = None
#     local_destino: Optional[str] = None
#     status: Optional[TipoStatus] = None
#     distancia: Optional[float] = None
#     combustivel_gasto: Optional[float] = None
#     custo_viagem: Optional[float] = None
#     observacoes: Optional[str] = None

#     veiculo: VeiculoMiniResponse | None = None

#     class Config:
#         from_attributes = True

# # ESTA É A CLASSE QUE RETORNA OS DADOS DETALHADOS
# class ViagemDetailResponse(ViagemBase):
#     id: str
#     motorista: MotoristaMini
#     veiculo: VeiculoMini
#     model_config = ConfigDict(from_attributes=True)

