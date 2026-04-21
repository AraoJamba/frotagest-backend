from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, Enum
from app.core.database import Base
import uuid
import enum
from datetime import datetime
from sqlalchemy.orm import relationship


class TipoVeiculo(str, enum.Enum):
    leve = "leve"
    medio = "medio"
    pesado = "pesado"
    
class Combustivel(str, enum.Enum):
    gasolina = "gasolina"
    diesel = "diesel"
    etanol = "etanol"
    
class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    placa = Column(String(15), unique=True, nullable=False)
    modelo = Column(String(100))
    marca = Column(String(100))
    ano = Column(Integer)
    VIN = Column(String(50), unique=True)
    tipo = Column(Enum(TipoVeiculo))
    capacidadeCarga = Column(Float)
    dataCadastro = Column(DateTime)
    ativo = Column(Boolean, default=True)
    combustivel = Column(Enum(Combustivel))
    consumoMedio = Column(Float)
    ultimaRevista = Column(DateTime)
    criadoEm = Column(DateTime, default=datetime.utcnow)
    
   
    viagens = relationship("Viagem", back_populates="veiculo")