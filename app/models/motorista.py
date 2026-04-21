import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Date
from app.core.database import Base


class Motorista(Base):
    __tablename__ = "motoristas"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefone = Column(String(50))

    numero_carta = Column(String(50), unique=True, nullable=False)
    numero_bi = Column(String(50), unique=True, nullable=False)

    categoria_carta = Column(String(10))
    
    data_nascimento = Column(Date)
    data_validade_carta = Column(Date)
    data_cadastro = Column(Date)

    ativo = Column(Boolean, default=True)

    endereco = Column(String(255))
    cidade = Column(String(100))
    provincia = Column(String(100))
    

# RELACIONAMENTO
    viagens = relationship("Viagem", back_populates="motorista")
    