from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TipoServico(str, Enum):
    manutencao = "manutencao"
    reparo = "reparo"
    inspecao = "inspecao"


class ServicoBase(BaseModel):
    nome: str
    descricao: str
    tipo: TipoServico
    custo_estimado: float
    ativo: bool


class ServicoCreate(ServicoBase):
    pass


class ServicoUpdate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):
    id: str
    data_cadastro: datetime

    class Config:
        from_attributes = True
