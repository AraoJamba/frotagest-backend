from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.viagem import ViagemDetailResponse
from app.models.viagem import Viagem

from sqlalchemy import func
from sqlalchemy import extract


from app.schemas.viagem import (
    ViagemCreate,
    ViagemUpdate,
    ViagemResponse
)

from app.crud import viagem as viagem_crud
from app.core.database import get_db


router = APIRouter(
    prefix="/viagens",
    tags=["Viagens"]
)


@router.post("/", response_model=ViagemResponse)
def criar(viagem: ViagemCreate, db: Session = Depends(get_db)):
    return viagem_crud.create_viagem(db, viagem)


@router.get("/", response_model=list[ViagemResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Viagem).join(Viagem.veiculo).all()


# @router.get("/")
# def listar(db: Session = Depends(get_db)):

#     viagens = db.query(Viagem).all()

#     resultado = []
    
#     for v in viagens:
#         resultado.append({
#             "id": v.id,
#             "motorista_id": v.motorista_id or "",
#             "veiculo_id": v.veiculo_id or "",
#             "dataInicio": v.data_inicio,
#             "dataFim": v.data_fim,
#             "localPartida": v.local_partida,
#             "localDestino": v.local_destino,
#             "distancia": v.distancia,
#             "status": v.status,
#             "combustivelGasto": v.combustivel_gasto,
#             "custoViagem": v.custo_viagem,
#         })




@router.get("/{viagem_id}", response_model=ViagemDetailResponse)
def buscar(viagem_id: str, db: Session = Depends(get_db)):
    viagem = viagem_crud.get_viagem_by_id(db, viagem_id)
    if not viagem:
        raise HTTPException(404, "Viagem não encontrada")
    return viagem




# @router.get("/{viagem_id}", response_model=ViagemResponse)
# def buscar(viagem_id: str, db: Session = Depends(get_db)):
#     viagem = viagem_crud.get_viagem_by_id(db, viagem_id)

#     if not viagem:
#         raise HTTPException(404, "Viagem não encontrada")

#     return viagem


@router.put("/{viagem_id}", response_model=ViagemResponse)
def atualizar(
    viagem_id: str,
    viagem: ViagemUpdate,
    db: Session = Depends(get_db)
):
    viagem_updated = viagem_crud.update_viagem(db, viagem_id, viagem)

    if not viagem_updated:
        raise HTTPException(404, "Viagem não encontrada")

    return viagem_updated


@router.delete("/{viagem_id}")
def deletar(viagem_id: str, db: Session = Depends(get_db)):
    viagem_deleted = viagem_crud.delete_viagem(db, viagem_id)

    if not viagem_deleted:
        raise HTTPException(404, "Viagem não encontrada")

    return {"message": "Viagem deletada com sucesso"}


@router.get("/estatisticas/resumo")
def resumo_viagens(db: Session = Depends(get_db)):

    planejadas = db.query(func.count(Viagem.id)).filter(
        Viagem.status == "planejada"
    ).scalar()

    andamento = db.query(func.count(Viagem.id)).filter(
        Viagem.status == "em_andamento"
    ).scalar()

    concluidas = db.query(func.count(Viagem.id)).filter(
        Viagem.status == "concluida"
    ).scalar()

    canceladas = db.query(func.count(Viagem.id)).filter(
        Viagem.status == "cancelada"
    ).scalar()

    total = db.query(func.count(Viagem.id)).scalar()

    return {
        "total": total,
        "planejadas": planejadas,
        "emAndamento": andamento,
        "concluidas": concluidas,
        "canceladas": canceladas
    }
    

@router.get("/analises/resumo")
def resumo_mensal_viagens(db: Session = Depends(get_db)):

    resultados = db.query(
        extract('month', Viagem.data_inicio).label('mes'),
        func.sum(Viagem.distancia).label('quilometragem'),
        func.sum(Viagem.custo_viagem).label('custo')
    ).group_by(
        'mes'
    ).all()

    meses_map = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    resposta = []

    for mes, km, custo in resultados:
        resposta.append({
            "mes": meses_map[int(mes)],
            "quilometragem": float(km or 0),
            "custo_viagem": float(custo or 0)
        })

    # ordena pelos meses
    resposta.sort(key=lambda x: list(meses_map.values()).index(x["mes"]))

    return resposta

@router.get("/analises/resumo/combustivel_gasto")
def combustivel_gasto_resumo(db: Session = Depends(get_db)):

    resultados = db.query(
        extract('month', Viagem.data_inicio).label('mes'),
        func.sum(Viagem.combustivel_gasto).label('combustivel_gasto')
    ).group_by(
        'mes'
    ).all()

    meses_map = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    resposta = []

    for mes, combustivel in resultados:
        resposta.append({
            "mes": meses_map[int(mes)],
            "combustivel_gasto": float(combustivel or 0)
        })

    # ordena pelos meses
    resposta.sort(key=lambda x: list(meses_map.values()).index(x["mes"]))

    return resposta


@router.get("/veiculo/{veiculo_id}")
def viagens_por_veiculo(veiculo_id: str, db: Session = Depends(get_db)):
    viagens = db.query(Viagem).filter(Viagem.veiculo_id == veiculo_id).all()

    resultado = []

    for v in viagens:
        resultado.append({
            "id": v.id,
            "motorista_id": v.motorista_id or "",
            "veiculo_id": v.veiculo_id or "",
            "dataInicio": v.data_inicio,
            "dataFim": v.data_fim,
            "localPartida": v.local_partida,
            "localDestino": v.local_destino,
            "distancia": v.distancia,
            "status": v.status,
            "combustivelGasto": v.combustivel_gasto,
            "custoViagem": v.custo_viagem,
        })

    return resultado


@router.get("/motorista/{motorista_id}")
def viagens_por_motorista(motorista_id: str, db: Session = Depends(get_db)):
    viagens = db.query(Viagem).filter(Viagem.motorista_id == motorista_id).all()

    resultado = []

    for v in viagens:
        resultado.append({
            "id": v.id,
            "motorista_id": v.motorista_id or "",
            "veiculo_id": v.veiculo_id or "",
            "dataInicio": v.data_inicio,
            "dataFim": v.data_fim,
            "localPartida": v.local_partida,
            "localDestino": v.local_destino,
            "distancia": v.distancia,
            "status": v.status,
            "combustivelGasto": v.combustivel_gasto,
            "custoViagem": v.custo_viagem,
        })

    return resultado



