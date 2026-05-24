from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


# =========================
# BASE
# =========================
class MotoristaBase(BaseModel):
    nome: str
    email: str
    telefone: str

    numero_carta: str
    numero_bi: str
    categoria_carta: str

    data_nascimento: date

    ativo: bool = True

    endereco: str
    cidade: str
    provincia: str


# =========================
# CREATE
# =========================
class MotoristaCreate(MotoristaBase):
    pass


# =========================
# UPDATE (PATCH REAL)
# =========================
class MotoristaUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None

    numero_carta: Optional[str] = None
    numero_bi: Optional[str] = None
    categoria_carta: Optional[str] = None

    data_nascimento: Optional[date] = None

    ativo: Optional[bool] = None

    endereco: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE
# =========================
class MotoristaResponse(BaseModel):
    id: str

    nome: str
    email: str
    telefone: str

    numero_carta: str
    numero_bi: str
    categoria_carta: str

    data_nascimento: date

    ativo: bool

    endereco: str
    cidade: str
    provincia: str

    model_config = ConfigDict(from_attributes=True)












# from pydantic import BaseModel
# from datetime import date


# class MotoristaBase(BaseModel):
#     nome: str
#     email: str
#     telefone: str
#     numero_carta: str
#     numero_bi: str
#     categoria_carta: str
#     data_nascimento: date
#     data_validade_carta: date
#     data_cadastro: date
#     ativo: bool
#     endereco: str
#     cidade: str
#     provincia: str
    

# class MotoristaCreate(MotoristaBase):
#     pass


# class MotoristaUpdate(MotoristaBase):
#     pass


# class MotoristaResponse(MotoristaBase):
#     id: str

#     class Config:
#         from_attributes = True