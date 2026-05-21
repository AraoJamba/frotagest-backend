from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


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
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    papel: Optional[PapelUsuario] = None


class UpdateSenha(BaseModel):
    senha_atual: str
    nova_senha: str

class UsuarioResponse(UsuarioBase):
    id: str

    class Config:
        from_attributes = True
