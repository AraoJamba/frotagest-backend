from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.core.database import get_db
from app.models.despesa import Despesa, TipoDespesa
from app.schemas.despesa import DespesaCreate, DespesaUpdate, DespesaResponse
from app.crud.despesa import create_despesa, update_despesa, delete_despesa


router = APIRouter(prefix="/despesas", tags=["Despesas"])


# =========================
# DEPENDENCY MULTI-TENANT
# =========================
def get_empresa_id(empresa_id: str = Cookie(None)):
    if not empresa_id:
        raise HTTPException(status_code=401, detail="Empresa não definida")
    return empresa_id


# =========================
# CRIAR DESPESA
# =========================
@router.post("/", response_model=DespesaResponse)
def criar(
    despesa: DespesaCreate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return create_despesa(db, despesa, empresa_id)


# =========================
# LISTAR DESPESAS
# =========================
@router.get("/", response_model=list[DespesaResponse])
def listar(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return db.query(Despesa).join(Despesa.veiculo).filter(
        Despesa.empresa_id == empresa_id
    ).all()


# =========================
# BUSCAR POR ID
# =========================
@router.get("/{despesa_id}", response_model=DespesaResponse)
def buscar(
    despesa_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    despesa = db.query(Despesa).join(Despesa.veiculo).filter(
        Despesa.id == despesa_id,
        Despesa.empresa_id == empresa_id
    ).first()

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return despesa


# =========================
# ATUALIZAR
# =========================
@router.put("/{despesa_id}", response_model=DespesaResponse)
def atualizar(
    despesa_id: str,
    despesa: DespesaUpdate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    despesa_atualizada = update_despesa(db, despesa_id, despesa, empresa_id)

    if not despesa_atualizada:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return despesa_atualizada


# =========================
# DELETE
# =========================
@router.delete("/{despesa_id}")
def deletar(
    despesa_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    despesa = delete_despesa(db, despesa_id, empresa_id)

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    return {"message": "Despesa deletada com sucesso"}


# =========================
# ESTATÍSTICAS
# =========================
@router.get("/estatisticas/resumo")
def resumo(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    total = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id
    ).scalar()

    pago = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.pago == True
    ).scalar()

    nao_pago = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.pago == False
    ).scalar()

    combustivel = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.combustivel
    ).scalar()

    lavagem = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.lavagem
    ).scalar()

    manutencao = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.manutencao
    ).scalar()

    seguro = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.seguro
    ).scalar()

    pneu = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.pneu
    ).scalar()

    outro = db.query(func.count(Despesa.id)).filter(
        Despesa.empresa_id == empresa_id,
        Despesa.tipo == TipoDespesa.outro
    ).scalar()

    return {
        "total": total,
        "pagos": pago,
        "nao_pago": nao_pago,
        "tipos": {
            "combustivel": combustivel,
            "pneus": pneu,
            "manutencoes": manutencao,
            "seguros": seguro,
            "lavagens": lavagem,
            "outros": outro
        }
    }


# =========================
# ANÁLISE MENSAL
# =========================
@router.get("/analises/resumo")
def analise_mensal(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    resultados = db.query(
        extract('month', Despesa.data).label('mes'),
        Despesa.tipo,
        func.sum(Despesa.valor).label('total')
    ).filter(
        Despesa.empresa_id == empresa_id
    ).group_by(
        'mes',
        Despesa.tipo
    ).all()

    meses_map = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    resposta = {}

    for mes, tipo, total in resultados:
        mes = int(mes)

        if mes not in resposta:
            resposta[mes] = {
                "mes": meses_map[mes],
                "combustivel": 0,
                "manutencao": 0,
                "seguro": 0,
                "pneu": 0,
                "lavagem": 0,
                "outro": 0
            }

        resposta[mes][tipo.value] = float(total)

    return sorted(
        resposta.values(),
        key=lambda x: list(meses_map.values()).index(x["mes"])
    )


# =========================
# POR VEÍCULO
# =========================
@router.get("/veiculo/{veiculo_id}", response_model=list[DespesaResponse])
def por_veiculo(
    veiculo_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return db.query(Despesa).join(Despesa.veiculo).filter(
        Despesa.veiculo_id == veiculo_id,
        Despesa.empresa_id == empresa_id
    ).all()





# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.schemas.despesa import DespesaCreate, DespesaUpdate, DespesaResponse
# from app.crud.despesa import create_despesa, delete_despesa, get_despesas, get_despesa_by_id, update_despesa

# from app.models.despesa import Despesa, TipoDespesa
# from sqlalchemy import func
# from sqlalchemy.orm import selectinload
# from sqlalchemy import extract

# from fastapi import Cookie, HTTPException

# def get_empresa_id(empresa_id: str = Cookie(None)):
#     if not empresa_id:
#         raise HTTPException(status_code=401, detail="Empresa não definida")
#     return empresa_id


# router = APIRouter(prefix="/despesas", tags=["Despesas"])


# @router.post("/", response_model=DespesaResponse)
# def criar(
#     despesa: DespesaCreate,
#     db: Session = Depends(get_db),
#     empresa_id: str = Depends(get_empresa_id)
# ):
#     return create_despesa(db, despesa, empresa_id)

# # @router.post("/", response_model=DespesaResponse)
# # def criar(despesa: DespesaCreate, db: Session = Depends(get_db)):
# #     return create_despesa(db, despesa)

# @router.get("/", response_model=list[DespesaResponse])
# def listar(
#     db: Session = Depends(get_db),
#     empresa_id: str = Depends(get_empresa_id)
# ):
#     return db.query(Despesa).join(Despesa.veiculo).filter(
#         Despesa.empresa_id == empresa_id
#     ).all()

# # @router.get("/", response_model=list[DespesaResponse])
# # def listar(db: Session = Depends(get_db)):
# #     return db.query(Despesa).join(Despesa.veiculo).all()

# #def listar(db: Session = Depends(get_db)):
# #   return get_despesas(db)


# @router.get("/{despesa_id}", response_model=DespesaResponse)
# def buscar(
#     despesa_id: str,
#     db: Session = Depends(get_db),
#     empresa_id: str = Depends(get_empresa_id)
# ):
#     return db.query(Despesa).join(Despesa.veiculo).filter(
#         Despesa.id == despesa_id,
#         Despesa.empresa_id == empresa_id
#     ).first()


# # @router.get("/{despesa_id}", response_model=DespesaResponse)
# # def buscar(despesa_id: str, db: Session = Depends(get_db)):
# #     return db.query(Despesa).join(Despesa.veiculo).filter(
# #         Despesa.id == despesa_id
# #     ).first()



# @router.put("/{despesa_id}", response_model=DespesaResponse)
# def atualizar(despesa_id: str, despesa: DespesaUpdate, db: Session = Depends(get_db)):
#     despesa_atualizada = update_despesa(db, despesa_id, despesa)

#     if not despesa_atualizada:
#         raise HTTPException(status_code=404, detail="Despesa não encontrada")

#     return despesa_atualizada


# @router.delete("/{despesa_id}")
# def deletar(despesa_id: str, db: Session = Depends(get_db)):
#     despesa = delete_despesa(db, despesa_id)

#     if not despesa:
#         raise HTTPException(status_code=404, detail="Despesa não encontrada")

#     return {"message": "Despesa deletada com sucesso"}




# @router.get("/estatisticas/resumo")
# def resumo_veiculos(db: Session = Depends(get_db)):

#     total = db.query(func.count(Despesa.id)).filter(
#         Despesa.empresa_id == empresa_id
#     ).scalar()

#     pago = db.query(func.count(Despesa.id)).filter(
#         Despesa.pago == True
#     ).scalar()

#     nao_pago = db.query(func.count(Despesa.id)).filter(
#         Despesa.pago == False
#     ).scalar()

#     #tipo
#     combustivel = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.combustivel
#     ).scalar()

#     lavagem = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.lavagem
#     ).scalar()

#     manutencao = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.manutencao
#     ).scalar()

#     seguro = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.seguro
#     ).scalar()

#     pneu = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.pneu
#     ).scalar()

#     outro = db.query(func.count(Despesa.id)).filter(
#         Despesa.tipo == TipoDespesa.outro
#     ).scalar()


#     return {
#         "total": total,
#         "pagos": pago,
#         "nao_pago": nao_pago,
 
#         "tipos": {
#             "combustivel": combustivel,
#             "pneus": pneu,
#             "manutencoes": manutencao,
#             "seguros": seguro,
#             "lavagens": lavagem,
#             "outros": outro
#         }
#     }




# @router.get("/analises/resumo")
# def resumo_mensal(db: Session = Depends(get_db)):

#     resultados = db.query(
#         extract('month', Despesa.data).label('mes'),
#         Despesa.tipo,
#         func.sum(Despesa.valor).label('total')
#     ).group_by(
#         'mes',
#         Despesa.tipo
#     ).all()

#     meses_map = {
#         1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
#         5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
#         9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
#     }

#     resposta = {}

#     for mes, tipo, total in resultados:
#         mes = int(mes)

#         if mes not in resposta:
#             resposta[mes] = {
#                 "mes": meses_map[mes],
#                 "combustivel": 0,
#                 "manutencao": 0,
#                 "seguro": 0,
#                 "pneu": 0,
#                 "lavagem": 0,
#                 "outro": 0
#             }

#         resposta[mes][tipo.value] = float(total)

#     return sorted(resposta.values(), key=lambda x: list(meses_map.values()).index(x["mes"]))


# @router.get("/veiculo/{veiculo_id}", response_model=list[DespesaResponse])
# def despesas_por_veiculo(veiculo_id: str, db: Session = Depends(get_db)):
#     return db.query(Despesa).join(Despesa.veiculo).filter(
#         Despesa.veiculo_id == veiculo_id
#     ).all()