
import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(String(50), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

    #motorista_id = Column(String(36), ForeignKey("motoristas.id"))

    #motoristas = relationship("Motorista", back_populates="viagens")
    
    #veiculo_id = Column(String(50), ForeignKey("veiculos.id"), nullable=False )

    data_inicio = Column(DateTime)
    data_fim = Column(DateTime, nullable=True)

    local_partida = Column(String(255))
    local_destino = Column(String(255))

    distancia = Column(Float)
    
    status = Column(String(20))

    combustivel_gasto = Column(Float)
    custo_viagem = Column(Float)

    observacoes = Column(String(500), nullable=True)
    
    
    # RELACIONAMENTOS
    motorista_id = Column(String(36), ForeignKey("motoristas.id"))
    veiculo_id = Column(String(36), ForeignKey("veiculos.id"))

    motorista = relationship("Motorista", back_populates="viagens")
    veiculo = relationship("Veiculo", back_populates="viagens")