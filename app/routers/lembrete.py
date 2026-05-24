from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.lembrete import Lembrete, TipoLembrete, PrioridadeLembrete
from app.schemas.lembrete import (
    LembreteCreate,
    LembreteUpdate,
    LembreteResponse
)
from app.crud import lembrete as lembrete_crud


router = APIRouter(prefix="/lembretes", tags=["Lembretes"])


# =========================
# MULTI-TENANT
# =========================
def get_empresa_id(empresa_id: str = Cookie(None)):
    if not empresa_id:
        raise HTTPException(status_code=401, detail="Empresa não definida")
    return empresa_id


# =========================
# CRIAR
# =========================
@router.post("/", response_model=LembreteResponse)
def criar(
    lembrete: LembreteCreate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return lembrete_crud.create_lembrete(db, lembrete, empresa_id)


# =========================
# LISTAR
# =========================
@router.get("/", response_model=list[LembreteResponse])
def listar(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return lembrete_crud.get_lembretes(db, empresa_id)


# =========================
# GET POR ID
# =========================
@router.get("/{lembrete_id}", response_model=LembreteResponse)
def pegar_por_id(
    lembrete_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    lembrete = lembrete_crud.get_lembrete_by_id(db, lembrete_id, empresa_id)

    if not lembrete:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return lembrete


# =========================
# UPDATE
# =========================
@router.put("/{lembrete_id}", response_model=LembreteResponse)
def atualizar(
    lembrete_id: str,
    lembrete: LembreteUpdate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    atualizado = lembrete_crud.update_lembrete(
        db,
        lembrete_id,
        lembrete,
        empresa_id
    )

    if not atualizado:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return atualizado


# =========================
# DELETE
# =========================
@router.delete("/{lembrete_id}")
def deletar(
    lembrete_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    removido = lembrete_crud.delete_lembrete(db, lembrete_id, empresa_id)

    if not removido:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")

    return {"message": "Lembrete deletado com sucesso"}


# =========================
# ESTATÍSTICAS
# =========================
@router.get("/estatisticas/resumo")
def resumo(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    total = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id
    ).scalar()

    completado = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.completado == True
    ).scalar()

    nao_completado = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.completado == False
    ).scalar()

    documentacao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.tipo == TipoLembrete.documentacao
    ).scalar()

    manutencao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.tipo == TipoLembrete.manutencao
    ).scalar()

    revisao = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.tipo == TipoLembrete.revisao
    ).scalar()

    outro = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.tipo == TipoLembrete.outro
    ).scalar()

    alta = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.prioridade == PrioridadeLembrete.alta
    ).scalar()

    media = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.prioridade == PrioridadeLembrete.media
    ).scalar()

    baixa = db.query(func.count(Lembrete.id)).filter(
        Lembrete.empresa_id == empresa_id,
        Lembrete.prioridade == PrioridadeLembrete.baixa
    ).scalar()

    return {
        "total": total,
        "completados": completado,
        "nao_completado": nao_completado,
        "prioridade": {
            "alta": alta,
            "media": media,
            "baixa": baixa
        },
        "tipos": {
            "documentacao": documentacao,
            "revisoes": revisao,
            "manutencoes": manutencao,
            "outros": outro
        }
    }





# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy import func

# from app.core.database import get_db
# from app.models.lembrete import Lembrete, TipoLembrete, PrioridadeLembrete
# from app.schemas.lembrete import (
#     LembreteCreate,
#     LembreteUpdate,
#     LembreteResponse
# )

# from app.crud import lembrete as lembrete_crud

# router = APIRouter(
#     prefix="/lembretes",
#     tags=["Lembretes"]
# )


# @router.post("/", response_model=LembreteResponse)
# def criar(lembrete: LembreteCreate, db: Session = Depends(get_db)):
#     return lembrete_crud.create_lembrete(db, lembrete)


# @router.get("/", response_model=list[LembreteResponse])
# def listar(db: Session = Depends(get_db)):
#     return lembrete_crud.get_lembretes(db)


# @router.get("/{lembrete_id}", response_model=LembreteResponse)
# def pegar_por_id(lembrete_id: str, db: Session = Depends(get_db)):
#     lembrete = lembrete_crud.get_lembrete_by_id(db, lembrete_id)

#     if not lembrete:
#         raise HTTPException(status_code=404, detail="Lembrete não encontrado")

#     return lembrete


# @router.put("/{lembrete_id}", response_model=LembreteResponse)
# def atualizar(
#     lembrete_id: str,
#     lembrete: LembreteUpdate,
#     db: Session = Depends(get_db)
# ):
#     lembrete_atualizado = lembrete_crud.update_lembrete(
#         db,
#         lembrete_id,
#         lembrete
#     )

#     if not lembrete_atualizado:
#         raise HTTPException(status_code=404, detail="Lembrete não encontrado")

#     return lembrete_atualizado


# @router.delete("/{lembrete_id}")
# def deletar(lembrete_id: str, db: Session = Depends(get_db)):
#     lembrete = lembrete_crud.delete_lembrete(db, lembrete_id)

#     if not lembrete:
#         raise HTTPException(status_code=404, detail="Lembrete não encontrado")

#     return {"message": "Lembrete deletado com sucesso"}


# @router.get("/estatisticas/resumo")
# def resumo_veiculos(db: Session = Depends(get_db)):

#     total = db.query(func.count(Lembrete.id)).scalar()

#     completado = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.completado == True
#     ).scalar()

#     nao_completado = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.completado == False
#     ).scalar()

#     #tipo
#     documentacao = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.tipo == TipoLembrete.documentacao
#     ).scalar()

#     manutencao = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.tipo == TipoLembrete.manutencao
#     ).scalar()

#     revisao = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.tipo == TipoLembrete.revisao
#     ).scalar()

#     outro = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.tipo == TipoLembrete.outro
#     ).scalar()

#     #prioridade
#     alta = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.prioridade == PrioridadeLembrete.alta
#     ).scalar()

#     media = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.prioridade == PrioridadeLembrete.media
#     ).scalar()

#     baixa = db.query(func.count(Lembrete.id)).filter(
#         Lembrete.prioridade == PrioridadeLembrete.baixa
#     ).scalar()


#     return {
#         "total": total,
#         "completados": completado,
#         "nao_completado": nao_completado,

#         "prioridade": {
#             "alta": alta,
#             "baixa": baixa,
#             "media": media
#         },
 
#         "tipos": {
#             "documentacao": documentacao,
#             "revisoes": revisao,
#             "manutencoes": manutencao,
#             "outros": outro
#         }
#     }
