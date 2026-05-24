from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# =========================
# BASE
# =========================
class EmpresaBase(BaseModel):
    nome: str
    nif: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None

    ativo: bool = True


# =========================
# CREATE
# =========================
# class EmpresaCreate(EmpresaBase):
#     pass

class EmpresaCreate(BaseModel):
    nome: str
    nif: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


# =========================
# UPDATE (PATCH REAL)
# =========================
class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    nif: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESPONSE
# =========================
class EmpresaResponse(BaseModel):
    id: str

    nome: str
    nif: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None


    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)










# from pydantic import BaseModel
# from typing import Optional


# class EmpresaCreate(BaseModel):
#     nome: str
#     nif: Optional[str] = None
#     telefone: Optional[str] = None
#     email: Optional[str] = None
#     endereco: Optional[str] = None