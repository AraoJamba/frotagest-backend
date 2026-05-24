from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.core.database import get_db
from app.models.posto_combustivel import PostoCombustivel

from app.schemas.posto_combustivel import (
    PostoCombustivelCreate,
    PostoCombustivelUpdate,
    PostoCombustivelResponse
)

from app.crud import posto_combustivel as posto_crud


router = APIRouter(prefix="/postos", tags=["Postos Combustivel"])


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
@router.post("/", response_model=PostoCombustivelResponse)
def criar(
    posto: PostoCombustivelCreate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return posto_crud.create_posto(db, posto, empresa_id)


# =========================
# LISTAR (com filtros)
# =========================
@router.get("/", response_model=list[PostoCombustivelResponse])
def listar(
    search: Optional[str] = None,
    nome: Optional[str] = None,
    cidade: Optional[str] = None,
    provincia: Optional[str] = None,
    gasoleo: Optional[str] = None,
    gasolina: Optional[str] = None,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return posto_crud.get_postos(
        db,
        empresa_id,
        search,
        nome,
        cidade,
        provincia,
        gasoleo,
        gasolina
    )


# =========================
# GET POR ID
# =========================
@router.get("/{posto_id}", response_model=PostoCombustivelResponse)
def pegar_por_id(
    posto_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    posto = posto_crud.get_posto_by_id(db, posto_id, empresa_id)

    if not posto:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return posto


# =========================
# UPDATE
# =========================
@router.put("/{posto_id}", response_model=PostoCombustivelResponse)
def atualizar(
    posto_id: str,
    posto: PostoCombustivelUpdate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    atualizado = posto_crud.update_posto(db, posto_id, posto, empresa_id)

    if not atualizado:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return atualizado


# =========================
# DELETE
# =========================
@router.delete("/{posto_id}")
def deletar(
    posto_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    removido = posto_crud.delete_posto(db, posto_id, empresa_id)

    if not removido:
        raise HTTPException(status_code=404, detail="Posto não encontrado")

    return {"message": "Posto deletado com sucesso"}


# =========================
# ESTATÍSTICAS
# =========================
@router.get("/estatisticas/resumo")
def resumo(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    total = db.query(func.count(PostoCombustivel.id)).filter(
        PostoCombustivel.empresa_id == empresa_id
    ).scalar()

    ativo = db.query(func.count(PostoCombustivel.id)).filter(
        PostoCombustivel.empresa_id == empresa_id,
        PostoCombustivel.ativo == True
    ).scalar()

    inativo = db.query(func.count(PostoCombustivel.id)).filter(
        PostoCombustivel.empresa_id == empresa_id,
        PostoCombustivel.ativo == False
    ).scalar()

    return {
        "total": total,
        "ativo": ativo,
        "inativo": inativo
    }






# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.core.database import get_db
# from app.schemas.posto_combustivel import (
#     PostoCombustivelCreate,
#     PostoCombustivelUpdate,
#     PostoCombustivelResponse
# )
# from app.crud import posto_combustivel as posto_crud
# from app.models.posto_combustivel import PostoCombustivel
# from typing import Optional
# from sqlalchemy import func


# router = APIRouter(
#     prefix="/postos",
#     tags=["Postos Combustivel"]
# )


# @router.post("/", response_model=PostoCombustivelResponse)
# def criar(posto: PostoCombustivelCreate, db: Session = Depends(get_db)):
#     return posto_crud.create_posto(db, posto)


# @router.get("/", response_model=list[PostoCombustivelResponse])
# def listar(
#     search: Optional[str] = None,
#     nome: Optional[str] = None,
#     cidade: Optional[str] = None,
#     provincia: Optional[str] = None,
#     gasoleo: Optional[str] = None,
#     gasolina: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     return posto_crud.get_postos(
#         db,
#         search,
#         nome,
#         cidade,
#         provincia,
#         gasoleo,
#         gasolina
#     )



# @router.get("/{posto_id}", response_model=PostoCombustivelResponse)
# def pegar_por_id(posto_id: str, db: Session = Depends(get_db)):
#     posto = posto_crud.get_posto_by_id(db, posto_id)

#     if not posto:
#         raise HTTPException(status_code=404, detail="Posto não encontrado")

#     return posto


# @router.put("/{posto_id}", response_model=PostoCombustivelResponse)
# def atualizar(
#     posto_id: str,
#     posto: PostoCombustivelUpdate,
#     db: Session = Depends(get_db)
# ):
#     posto_atualizado = posto_crud.update_posto(db, posto_id, posto)

#     if not posto_atualizado:
#         raise HTTPException(status_code=404, detail="Posto não encontrado")

#     return posto_atualizado


# @router.delete("/{posto_id}")
# def deletar(posto_id: str, db: Session = Depends(get_db)):
#     posto = posto_crud.delete_posto(db, posto_id)

#     if not posto:
#         raise HTTPException(status_code=404, detail="Posto não encontrado")

#     return {"message": "Posto deletado com sucesso"}

# @router.get("/estatisticas/resumo")
# def resumo_veiculos(db: Session = Depends(get_db)):

#     total = db.query(func.count(PostoCombustivel.id)).scalar()

#     ativo = db.query(func.count(PostoCombustivel.id)).filter(
#         PostoCombustivel.ativo == True
#     ).scalar()

#     inativo = db.query(func.count(PostoCombustivel.id)).filter(
#         PostoCombustivel.ativo == False
#     ).scalar()



#     return {
#         "total": total,
#         "ativo": ativo,
#         "inativo": inativo,
#     }

