from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


class LoginResponse(BaseModel):
    id: str
    nome: str
    email: str
    papel: str
