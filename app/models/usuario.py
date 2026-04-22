import uuid
import enum

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import CHAR

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

    papel = Column(
        Enum(PapelUsuario),
        nullable=False
    )
