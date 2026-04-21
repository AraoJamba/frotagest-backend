from pydantic import BaseModel
from datetime import date


class MotoristaBase(BaseModel):
    nome: str
    email: str
    telefone: str
    numero_carta: str
    numero_bi: str
    categoria_carta: str
    data_nascimento: date
    data_validade_carta: date
    data_cadastro: date
    ativo: bool
    endereco: str
    cidade: str
    provincia: str
    

class MotoristaCreate(MotoristaBase):
    pass


class MotoristaUpdate(MotoristaBase):
    pass


class MotoristaResponse(MotoristaBase):
    id: str

    class Config:
        from_attributes = True