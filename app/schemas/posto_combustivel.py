from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class PostoCombustivelBase(BaseModel):
    nome: str
    endereco: str
    cidade: str
    provincia: str
    telefone: Optional[str] = None
    preco_combustivel: float
    gasoleo: float
    gasolina: float
    data_cadastro: date
    ativo: bool


class PostoCombustivelCreate(PostoCombustivelBase):
    pass


class PostoCombustivelUpdate(PostoCombustivelBase):
    pass


class PostoCombustivelResponse(PostoCombustivelBase):
    id: str
    criado_em: datetime

    class Config:
        from_attributes = True
