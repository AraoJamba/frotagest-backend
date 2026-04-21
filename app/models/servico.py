from sqlalchemy import Column, String, Boolean, Date
from app.core.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(String(36), primary_key=True)
    nome = Column(String(255))
    descricao = Column(String(255))
    tipo = Column(String(50))
    custoEstimado = Column(Float)
    dataCadastro = Column(Date)
    ativo = Column(Boolean, default=True)
