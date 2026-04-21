from fastapi import FastAPI
from app.routers import veiculo
from app.core.database import engine
from app.core.database import Base
from app.routers import motorista
from app.routers import viagem
from app.routers import posto_combustivel
from app.routers import lembrete
from app.routers import despesa




app = FastAPI()




app.include_router(despesa.router)
app.include_router(lembrete.router)
app.include_router(viagem.router)
app.include_router(veiculo.router)
app.include_router(motorista.router)
app.include_router(posto_combustivel.router)

# Base.metadata.create_all(bind=engine)