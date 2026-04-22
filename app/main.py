from fastapi import FastAPI
from app.routers import veiculo
from app.core.database import engine
from app.core.database import Base
from app.routers import motorista
from app.routers import viagem
from app.routers import posto_combustivel
from app.routers import lembrete
from app.routers import despesa
from app.routers import manutencao_veiculo
from app.routers import servico
from app.routers import configuracoes_empresa
from app.routers import configuracoes_medidas
from app.routers import usuario
from app.routers import auth

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(configuracoes_medidas.router)
app.include_router(configuracoes_empresa.router)
app.include_router(servico.router)
app.include_router(manutencao_veiculo.router)
app.include_router(despesa.router)
app.include_router(lembrete.router)
app.include_router(viagem.router)
app.include_router(veiculo.router)
app.include_router(motorista.router)
app.include_router(posto_combustivel.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API rodando"}