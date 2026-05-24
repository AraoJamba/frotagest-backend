import uuid
import enum

from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class PapelUsuario(str, enum.Enum):
    admin = "admin"
    gerente = "gerente"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    empresa_id = Column(
        String(36),
        ForeignKey("empresas.id"),
        nullable=False
    )

    papel = Column(
        SQLEnum(PapelUsuario),
        nullable=False,
        default=PapelUsuario.gerente
    )

    empresa = relationship(
        "Empresa",
        back_populates="usuarios"
    )