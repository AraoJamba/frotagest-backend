from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from app.schemas.veiculo import VeiculoMiniResponse


class TipoManutencao(str, Enum):
    preventiva = "preventiva"
    corretiva = "corretiva"
    manutencao = "manutencao"
    reparo = "reparo"
    inspecao = "inspecao"



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


class ManutencaoResponse(BaseModel):
    id: str
    veiculo_id: str

    tipo_manutencao: str
    descricao: str

    data_agendada: datetime
    data_conclusao: datetime | None

    responsavel: str
    custo: float
    status: str

    criado_em: datetime | None

    veiculo: VeiculoMiniResponse | None = None

    class Config:
        from_attributes = True
