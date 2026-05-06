from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class TipoStatus (str, Enum):
    planejada = 'planejada'
    em_andamento = 'em_andamento'
    concluida = 'concluida'
    cancelada = 'cancelada'

class MotoristaMini(BaseModel):
    id: Optional[str] = None
    nome: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class VeiculoMini(BaseModel):
    id: Optional[str] = None
    placa: str
    marca: str
    modelo: str
    model_config = ConfigDict(from_attributes=True)

# --- Schemas da Viagem ---

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

class ViagemCreate(ViagemBase):
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None

class ViagemUpdate(BaseModel):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    local_partida: Optional[str] = None
    local_destino: Optional[str] = None
    status: Optional[TipoStatus] = None
    distancia: Optional[float] = None
    combustivel_gasto: Optional[float] = None
    custo_viagem: Optional[float] = None
    observacoes: Optional[str] = None

class ViagemResponse(ViagemBase):
    id: str
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ESTA É A CLASSE QUE RETORNA OS DADOS DETALHADOS
class ViagemDetailResponse(ViagemBase):
    id: str
    motorista: MotoristaMini
    veiculo: VeiculoMini
    model_config = ConfigDict(from_attributes=True)

