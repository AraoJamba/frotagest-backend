from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from typing import Optional


# =========================
# ENUM
# =========================
class PapelUsuario(str, Enum):
    admin = "admin"
    gerente = "gerente"


# =========================
# BASE
# =========================
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    papel: PapelUsuario
    empresa_id: str


# =========================
# CREATE INTERNO (ADMIN FLOW)
# =========================
class UsuarioCreate(UsuarioBase):
    senha: str
    empresa_id: str


# =========================
# REGISTRO PÚBLICO (SETUP INICIAL)
# =========================
class UsuarioRegistro(BaseModel):
    nome: str
    email: EmailStr
    senha: str



# =========================
# UPDATE
# =========================
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    papel: Optional[PapelUsuario] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# ALTERAR SENHA
# =========================
class UpdateSenha(BaseModel):
    senha_atual: str
    nova_senha: str


# =========================
# RESPONSE
# =========================
class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    papel: PapelUsuario

    model_config = ConfigDict(from_attributes=True)














# from pydantic import BaseModel, EmailStr
# from enum import Enum
# from typing import Optional


# class PapelUsuario(str, Enum):
#     admin = "admin"
#     gerente = "gerente"


# # =========================
# # BASE
# # =========================

# class UsuarioBase(BaseModel):
#     nome: str
#     email: EmailStr


# # =========================
# # CRIAÇÃO INTERNA
# # ADMIN cria gerente/admin
# # =========================

# class UsuarioCreate(UsuarioBase):
#     senha: str
#     papel: PapelUsuario = PapelUsuario.gerente


# # =========================
# # REGISTRO INICIAL
# # EMPRESA + ADMIN
# # =========================

# class UsuarioRegistro(BaseModel):
#     nome: str
#     email: EmailStr
#     senha: str


# # =========================
# # UPDATE
# # =========================

# class UsuarioUpdate(BaseModel):
#     nome: Optional[str] = None
#     email: Optional[EmailStr] = None
#     senha: Optional[str] = None
#     papel: Optional[PapelUsuario] = None


# # =========================
# # ALTERAR SENHA
# # =========================

# class UpdateSenha(BaseModel):
#     senha_atual: str
#     nova_senha: str


# # =========================
# # RESPONSE
# # =========================

# class UsuarioResponse(UsuarioBase):
#     id: str
#     papel: PapelUsuario

#     class Config:
#         from_attributes = True






# # from pydantic import BaseModel, EmailStr
# # from enum import Enum
# # from typing import Optional


# # class PapelUsuario(str, Enum):
# #     admin = "admin"
# #     gerente = "gerente"


# # class UsuarioBase(BaseModel):
# #     nome: str
# #     email: EmailStr
# #     papel: PapelUsuario


# # class UsuarioCreate(UsuarioBase):
# #     senha: str


# # class UsuarioUpdate(BaseModel):
# #     nome: Optional[str] = None
# #     email: Optional[EmailStr] = None
# #     senha: Optional[str] = None
# #     papel: Optional[PapelUsuario] = None


# # class UpdateSenha(BaseModel):
# #     senha_atual: str
# #     nova_senha: str

# # class UsuarioResponse(UsuarioBase):
# #     id: str

# #     class Config:
# #         from_attributes = True
