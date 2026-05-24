import uuid

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    ForeignKey,
    Float,
    DateTime
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class PostoCombustivel(Base):
    __tablename__ = "postos_combustivel"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    nome = Column(
        String(255),
        nullable=False
    )

    endereco = Column(
        String(255),
        nullable=True
    )

    cidade = Column(
        String(100),
        nullable=True
    )

    provincia = Column(
        String(100),
        nullable=True
    )

    telefone = Column(
        String(50),
        nullable=True
    )

    gasoleo = Column(
        Float,
        nullable=True
    )

    empresa_id = Column(
        String(36),
        ForeignKey("empresas.id"),
        nullable=False
    )

    gasolina = Column(
        Float,
        nullable=True
    )

    ativo = Column(
        Boolean,
        default=True
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )





    empresa = relationship(
        "Empresa",
        back_populates="postos_combustivel"
    )





# import uuid
# from sqlalchemy import Column, String, Boolean, Float, Date, DateTime
# from datetime import datetime
# from app.core.database import Base


# class PostoCombustivel(Base):
#     __tablename__ = "postos_combustivel"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

#     nome = Column(String(255))
#     endereco = Column(String(255))
#     cidade = Column(String(100))
#     provincia = Column(String(100))

#     telefone = Column(String(50), nullable=True)

#     preco_combustivel = Column(Float)
#     gasoleo = Column(Float)
#     gasolina = Column(Float)

#     data_cadastro = Column(Date)

#     ativo = Column(Boolean, default=True)

#     criado_em = Column(DateTime, default=datetime.utcnow)


