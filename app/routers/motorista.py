from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.motorista import Motorista
from app.models.viagem import Viagem

from app.schemas.motorista import (
    MotoristaCreate,
    MotoristaUpdate,
    MotoristaResponse
)

from app.crud.motorista import (
    create_motorista,
    get_motoristas,
    get_motorista_by_id,
    update_motorista,
    delete_motorista
)

router = APIRouter(prefix="/motoristas", tags=["Motoristas"])


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
@router.post("/", response_model=MotoristaResponse)
def create(
    motorista: MotoristaCreate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return create_motorista(db, motorista, empresa_id)


# =========================
# LISTAR (com filtros)
# =========================
@router.get("/", response_model=list[MotoristaResponse])
def listar(
    search: str = None,
    email: str = None,
    telefone: str = None,
    numero_carta: str = None,
    numero_bi: str = None,
    categoria_carta: str = None,
    provincia: str = None,
    data_nascimento: str = None,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return get_motoristas(
        db,
        empresa_id,
        search,
        email,
        telefone,
        numero_carta,
        numero_bi,
        categoria_carta,
        provincia,
        data_nascimento
    )


# =========================
# GET POR ID
# =========================
@router.get("/{motorista_id}", response_model=MotoristaResponse)
def get_by_id(
    motorista_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    motorista = get_motorista_by_id(db, motorista_id, empresa_id)

    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    return motorista


# =========================
# UPDATE
# =========================
@router.put("/{motorista_id}", response_model=MotoristaResponse)
def update(
    motorista_id: str,
    motorista: MotoristaUpdate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    atualizado = update_motorista(db, motorista_id, motorista, empresa_id)

    if not atualizado:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    return atualizado


# =========================
# DELETE (corrigido)
# =========================
@router.delete("/{motorista_id}")
def deletar(
    motorista_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    # verificar viagens dentro da empresa
    viagens = db.query(Viagem).filter(
        Viagem.motorista_id == motorista_id,
        Viagem.empresa_id == empresa_id
    ).all()

    if len(viagens) > 0:
        raise HTTPException(
            status_code=400,
            detail="Motorista possui viagens associadas"
        )

    motorista = db.query(Motorista).filter(
        Motorista.id == motorista_id,
        Motorista.empresa_id == empresa_id
    ).first()

    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    db.delete(motorista)
    db.commit()

    return {"message": "Motorista deletado com sucesso"}


# =========================
# ESTATÍSTICAS
# =========================
@router.get("/estatisticas/resumo")
def resumo(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    total = db.query(func.count(Motorista.id)).filter(
        Motorista.empresa_id == empresa_id
    ).scalar()

    ativos = db.query(func.count(Motorista.id)).filter(
        Motorista.empresa_id == empresa_id,
        Motorista.ativo == True
    ).scalar()

    inativos = db.query(func.count(Motorista.id)).filter(
        Motorista.empresa_id == empresa_id,
        Motorista.ativo == False
    ).scalar()

    return {
        "total": total,
        "ativos": ativos,
        "inativos": inativos
    }







# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models.viagem import Viagem
# from app.models.motorista import Motorista 



# from app.schemas.motorista import (
#     MotoristaCreate,
#     MotoristaUpdate,
#     MotoristaResponse
# )

# from app.crud.motorista import (
#     create_motorista,
#     get_motoristas,
#     get_motorista_by_id,
#     update_motorista,
#     delete_motorista
# )

# from app.core.database import get_db

# from sqlalchemy import func

# router = APIRouter(
#     prefix="/motoristas",
#     tags=["Motoristas"]
# )


# @router.post("/", response_model=MotoristaResponse)
# def create(motorista: MotoristaCreate, db: Session = Depends(get_db)):
#     return create_motorista(db, motorista)


# from typing import Optional

# @router.get("/", response_model=list[MotoristaResponse])
# def listar(
#     search: Optional[str] = None,
#     email: Optional[str] = None,
#     telefone: Optional[str] = None,
#     numero_carta: Optional[str] = None,
#     numero_bi: Optional[str] = None,
#     categoria_carta: Optional[str] = None,
#     provincia: Optional[str] = None,
#     data_nascimento: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     return get_motoristas(
#         db,
#         search,
#         email,
#         telefone,
#         numero_carta,
#         numero_bi,
#         categoria_carta,
#         provincia,
#         data_nascimento
#     )



# @router.get("/{motorista_id}", response_model=MotoristaResponse)
# def get_by_id(motorista_id: str, db: Session = Depends(get_db)):
#     motorista = get_motorista_by_id(db, motorista_id)
    
#     if not motorista:
#         raise HTTPException(404, "Motorista não encontrado")

#     return motorista

# @router.put("/{motorista_id}", response_model=MotoristaResponse)
# def update(
#     motorista_id: str,
#     motorista: MotoristaUpdate,
#     db: Session = Depends(get_db)
# ):
#     motorista_updated = update_motorista(db, motorista_id, motorista)

#     if not motorista_updated:
#         raise HTTPException(404, "Motorista não encontrado")

#     return motorista_updated


# @router.delete("/motoristas/{id}")
# def deletar_motorista(id: str, db: Session = Depends(get_db)):
    
#     # 🔴 verificar se tem viagens associadas
#     viagens = db.query(Viagem).filter(Viagem.motorista_id == id).all()

#     if len(viagens) > 0:
#         raise HTTPException(
#             status_code=400,
#             detail="Motorista possui viagens associadas"
#         )

#     # ✅ deletar motorista
#     motorista = db.query(Motorista).filter(Motorista.id == id).first()

#     if not motorista:
#         raise HTTPException(status_code=404, detail="Motorista não encontrado")

#     db.delete(motorista)
#     db.commit()

#     return {"message": "Motorista deletado com sucesso"}




# @router.get("/estatisticas/resumo")
# def resumo_veiculos(db: Session = Depends(get_db)):

#     total = db.query(func.count(Motorista.id)).scalar()

#     activos = db.query(func.count(Motorista.id)).filter(
#         Motorista.ativo == True
#     ).scalar()

#     inactivos = db.query(func.count(Motorista.id)).filter(
#         Motorista.ativo == False
#     ).scalar()


#     return {
#         "total": total,
#         "ativos": activos,
#         "inativos": inactivos,
#     }

# #onestate
