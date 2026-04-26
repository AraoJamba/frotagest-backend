from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# --- Schemas para aninhamento (Dados do Motorista e Veículo) ---

class MotoristaMini(BaseModel):
    id: str
    nome: str
    model_config = ConfigDict(from_attributes=True)

class VeiculoMini(BaseModel):
    id: str
    placa: str
    marca: str
    modelo: str
    model_config = ConfigDict(from_attributes=True)

# --- Schemas da Viagem ---

class ViagemBase(BaseModel):
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    local_partida: str
    local_destino: str
    distancia: float
    status: str
    combustivel_gasto: float
    custo_viagem: float
    observacoes: Optional[str] = None

class ViagemCreate(ViagemBase):
    motorista_id: str
    veiculo_id: str

class ViagemUpdate(BaseModel):
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    local_partida: Optional[str] = None
    local_destino: Optional[str] = None
    status: Optional[str] = None
    distancia: Optional[float] = None
    combustivel_gasto: Optional[float] = None
    custo_viagem: Optional[float] = None
    observacoes: Optional[str] = None

class ViagemResponse(ViagemBase):
    id: str
    motorista_id: str
    veiculo_id: str
    model_config = ConfigDict(from_attributes=True)

# ESTA É A CLASSE QUE RETORNA OS DADOS DETALHADOS
class ViagemDetailResponse(ViagemBase):
    id: str
    motorista: MotoristaMini
    veiculo: VeiculoMini
    model_config = ConfigDict(from_attributes=True)






# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime



# class MotoristaMini(BaseModel):
#     id: str
#     nome: str

#     model_config = {
#         "from_attributes": True
#     }


# class VeiculoMini(BaseModel):
#     id: str
#     placa: str
#     modelo: str
#     marca: str

#     model_config = {
#         "from_attributes": True
#     }



# class ViagemBase(BaseModel):

#     motorista: MotoristaMini
#     veiculo: VeiculoMini
#     data_inicio: datetime
#     data_fim: Optional[datetime] = None
#     local_partida: str
#     local_destino: str
#     distancia: float
#     status: str
#     combustivel_gasto: float
#     custo_viagem: float
#     observacoes: Optional[str] = None
    
    
# class ViagemDetailResponse(ViagemBase):
#     id: str
#     motorista: MotoristaMini
#     veiculo: VeiculoMini

#     class Config:
#         from_attributes = True
    
    
# class ViagemCreate(ViagemBase):
#     pass


# class ViagemUpdate(BaseModel):
   
#     motorista: MotoristaMini
#     veiculo: VeiculoMini
#     data_inicio: Optional[datetime] = None
#     data_fim: Optional[datetime] = None
#     local_partida: Optional[str] = None
#     local_destino: Optional[str] = None
#     distancia: Optional[float] = None
#     status: Optional[str] = None
#     combustivel_gasto: Optional[float] = None
#     custo_viagem: Optional[float] = None
#     observacoes: Optional[str] = None
    
# class ViagemResponse(ViagemBase):
#     id: str

#     class Config:
#         from_attributes = True


