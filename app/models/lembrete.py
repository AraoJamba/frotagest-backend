import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Lembrete(Base):
    __tablename__ = "lembretes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    titulo = Column(String(255))
    descricao = Column(String(500))
    tipo = Column(String(50))

    data_agendada = Column(DateTime)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    completado = Column(Boolean, default=False)

    prioridade = Column(String(20))

    veiculo_id = Column(String(36), ForeignKey("veiculos.id"), nullable=True)
    motorista_id = Column(String(36), ForeignKey("motoristas.id"), nullable=True)

    # Relacionamentos
    veiculo = relationship("Veiculo")
    motorista = relationship("Motorista")
