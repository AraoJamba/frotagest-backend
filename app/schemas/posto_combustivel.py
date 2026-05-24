from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


# =========================
# BASE
# =========================
class PostoCombustivelBase(BaseModel):
    nome: str
    endereco: str
    cidade: str
    provincia: str

    telefone: Optional[str] = None

    gasoleo: float
    gasolina: float

    ativo: bool = True


# =========================
# CREATE
# =========================
class PostoCombustivelCreate(PostoCombustivelBase):
    pass


# =========================
# UPDATE (PATCH REAL)
# =========================
class PostoCombustivelUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None

    telefone: Optional[str] = None

    gasoleo: Optional[float] = None
    gasolina: Optional[float] = None

    ativo: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE
# =========================
class PostoCombustivelResponse(PostoCombustivelBase):
    id: str

    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)






# from pydantic import BaseModel
# from datetime import date, datetime
# from typing import Optional


# class PostoCombustivelBase(BaseModel):
#     nome: str
#     endereco: str
#     cidade: str
#     provincia: str
#     telefone: Optional[str] = None
#     preco_combustivel: float
#     gasoleo: float
#     gasolina: float
#     data_cadastro: date
#     ativo: bool


# class PostoCombustivelCreate(PostoCombustivelBase):
#     pass


# class PostoCombustivelUpdate(PostoCombustivelBase):
#     pass


# class PostoCombustivelResponse(PostoCombustivelBase):
#     id: str
#     criado_em: datetime

#     class Config:
#         from_attributes = True
