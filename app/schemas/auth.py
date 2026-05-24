from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr
from app.schemas.empresa import EmpresaCreate
from app.schemas.usuario import UsuarioRegistro


class RegistroEmpresaAdmin(BaseModel):
    empresa: EmpresaCreate

    usuario: UsuarioRegistro


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


class LoginResponse(BaseModel):
    id: str
    nome: str
    email: str
    papel: str
