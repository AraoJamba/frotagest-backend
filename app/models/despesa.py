import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, nullable=False)
    descricao = Column(String(255), nullable=False)
    recibo = Column(String(255), nullable=True)
    pago = Column(Boolean, default=False)

    veiculo_id = Column(String(36), ForeignKey("veiculos.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
