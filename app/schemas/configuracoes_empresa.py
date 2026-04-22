from pydantic import BaseModel, EmailStr
from typing import Optional


class ConfiguracoesEmpresaBase(BaseModel):
    nome_empresa: str
    nif: str
    endereco: str
    telefone: str
    email: EmailStr
    logo_url: Optional[str] = None


class ConfiguracoesEmpresaCreate(ConfiguracoesEmpresaBase):
    pass


class ConfiguracoesEmpresaUpdate(ConfiguracoesEmpresaBase):
    pass


class ConfiguracoesEmpresaResponse(ConfiguracoesEmpresaBase):
    id: str

    class Config:
        from_attributes = True
