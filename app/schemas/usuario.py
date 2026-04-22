from pydantic import BaseModel, EmailStr
from enum import Enum


class PapelUsuario(str, Enum):
    admin = "admin"
    gerente = "gerente"


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    papel: PapelUsuario


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    papel: PapelUsuario


class UsuarioResponse(UsuarioBase):
    id: str

    class Config:
        from_attributes = True
