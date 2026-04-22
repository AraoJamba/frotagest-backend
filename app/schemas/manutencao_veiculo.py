from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TipoManutencao(str, Enum):
    preventiva = "preventiva"
    corretiva = "corretiva"


class StatusManutencao(str, Enum):
    agendada = "agendada"
    emAndamento = "emAndamento"
    concluida = "concluida"
    cancelada = "cancelada"


class ManutencaoBase(BaseModel):
    veiculo_id: str
    tipo_manutencao: TipoManutencao
    descricao: str
    data_agendada: datetime
    data_conclusao: Optional[datetime] = None
    responsavel: str
    custo: float
    status: StatusManutencao


class ManutencaoCreate(ManutencaoBase):
    pass


class ManutencaoUpdate(ManutencaoBase):
    pass


class ManutencaoResponse(ManutencaoBase):
    id: str

    class Config:
        from_attributes = True
