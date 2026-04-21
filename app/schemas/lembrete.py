from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LembreteBase(BaseModel):
    titulo: str
    descricao: str
    tipo: str
    data_agendada: datetime
    completado: bool
    veiculo_id: Optional[str] = None
    motorista_id: Optional[str] = None
    prioridade: str


class LembreteCreate(LembreteBase):
    pass


class LembreteUpdate(LembreteBase):
    pass


class LembreteResponse(LembreteBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True
