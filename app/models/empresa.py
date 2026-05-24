# models/empresa.py

import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    nome = Column(String(150), nullable=False)

    nif = Column(String(50), unique=True, nullable=True)

    telefone = Column(String(50), nullable=True)

    email = Column(String(100), nullable=True)

    endereco = Column(String(255), nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())




    # Relacionamentos
    usuarios = relationship("Usuario", back_populates="empresa")

    veiculos = relationship("Veiculo", back_populates="empresa")

    motoristas = relationship("Motorista", back_populates="empresa")

    viagens = relationship("Viagem", back_populates="empresa")

    despesas = relationship("Despesa", back_populates="empresa")

    manutencoes = relationship("ManutencaoVeiculo", back_populates="empresa")

    postos_combustivel = relationship("PostoCombustivel", back_populates="empresa")

    lembretes = relationship("Lembrete", back_populates="empresa")