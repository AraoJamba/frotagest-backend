import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR

from app.core.database import Base


class ConfiguracoesEmpresa(Base):
    __tablename__ = "configuracoes_empresa"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    nome_empresa = Column(String(150), nullable=False)

    nif = Column(String(50), nullable=False)

    endereco = Column(String(255), nullable=False)

    telefone = Column(String(50), nullable=False)

    email = Column(String(100), nullable=False)

    logo_url = Column(String(255), nullable=True)
