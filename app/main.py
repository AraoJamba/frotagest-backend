from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base
from app.routers import (
    veiculo,
    motorista,
    viagem,
    posto_combustivel,
    lembrete,
    despesa,
    manutencao_veiculo,
    servico,
    configuracoes_empresa,
    configuracoes_medidas,
    usuario,
    auth
)



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