from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

import os
from dotenv import load_dotenv


from alembic import context
from app.core.database import Base

from app.models.veiculo import Veiculo
from app.models.despesa import Despesa
from app.models.viagem import Viagem
from app.models.motorista import Motorista
from app.models.manutencao_veiculo import ManutencaoVeiculo
from app.models.servico import Servico
from app.models.usuario import Usuario
from app.models.lembrete import Lembrete
from app.models.empresa import Empresa
from app.models.configuracoes_empresa import ConfiguracoesEmpresa
from app.models.configuracoes_medidas import ConfiguracoesMedidas
from app.models.posto_combustivel import PostoCombustivel




load_dotenv()


config = context.config

config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

target_metadata = Base.metadata





config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()





def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
