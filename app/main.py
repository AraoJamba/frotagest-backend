from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    veiculo, motorista, viagem, posto_combustivel, 
    lembrete, despesa, manutencao_veiculo, servico, 
    configuracoes_empresa, configuracoes_medidas, usuario, auth
)

# 1. Crie a instância APENAS UMA VEZ
app = FastAPI()

# 2. Configure o CORS IMEDIATAMENTE após criar o app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,  # ESSENCIAL para os Cookies que você está usando
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclua as rotas (O app agora possui o CORS e as rotas)
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

@app.get("/")
def root():
    return {"message": "API rodando"}