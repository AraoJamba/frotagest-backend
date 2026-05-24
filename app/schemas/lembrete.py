from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


# =========================
# ENUMS
# =========================
class TipoLembrete(str, Enum):
    documentacao = "documentacao"
    manutencao = "manutencao"
    revisao = "revisao"
    outro = "outro"


class PrioridadeLembrete(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


# =========================
# BASE
# =========================
class LembreteBase(BaseModel):
    titulo: str
    descricao: str

    tipo: TipoLembrete
    prioridade: PrioridadeLembrete

    data_agendada: datetime

    completado: bool = False

    veiculo_id: Optional[str] = None


# =========================
# CREATE
# =========================
class LembreteCreate(LembreteBase):
    pass


# =========================
# UPDATE (PATCH REAL)
# =========================
class LembreteUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None

    tipo: Optional[TipoLembrete] = None
    prioridade: Optional[PrioridadeLembrete] = None

    data_agendada: Optional[datetime] = None
    completado: Optional[bool] = None

    veiculo_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE
# =========================
class LembreteResponse(BaseModel):
    id: str

    titulo: str
    descricao: str

    tipo: TipoLembrete
    prioridade: PrioridadeLembrete

    data_agendada: datetime
    completado: bool

    veiculo_id: Optional[str] = None

    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)











# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional


# class LembreteBase(BaseModel):
#     titulo: str
#     descricao: str
#     tipo: str
#     data_agendada: datetime
#     completado: bool
#     veiculo_id: Optional[str] = None
#     motorista_id: Optional[str] = None
#     prioridade: str


# class LembreteCreate(LembreteBase):
#     pass


# class LembreteUpdate(LembreteBase):
#     pass


# class LembreteResponse(LembreteBase):
#     id: str
#     data_criacao: datetime

#     class Config:
#         from_attributes = True
