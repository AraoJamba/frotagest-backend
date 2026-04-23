from pydantic import BaseModel
from typing import Optional
from datetime import datetime






class ViagemBase(BaseModel):
    motorista_id: str
    veiculo_id: str
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    local_partida: str
    local_destino: str
    distancia: float
    status: str
    combustivel_gasto: float
    custo_viagem: float
    observacoes: Optional[str] = None
    
    
class ViagemCreate(ViagemBase):
    pass


class ViagemUpdate(BaseModel):
    motorista_id: Optional[str] = None
    veiculo_id: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    local_partida: Optional[str] = None
    local_destino: Optional[str] = None
    distancia: Optional[float] = None
    status: Optional[str] = None
    combustivel_gasto: Optional[float] = None
    custo_viagem: Optional[float] = None
    observacoes: Optional[str] = None
    
class ViagemResponse(ViagemBase):
    id: str

    class Config:
        from_attributes = True
