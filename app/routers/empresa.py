from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.empresa import Empresa

from app.schemas.empresa import (
    EmpresaCreate,
    EmpresaUpdate,
    EmpresaResponse
)

from app.crud import empresa as crud


router = APIRouter(prefix="/empresas", tags=["Empresas"])


# =========================
# MULTI-TENANT (contexto atual)
# =========================
def get_empresa_id(empresa_id: str = Cookie(None)):
    if not empresa_id:
        raise HTTPException(status_code=401, detail="Empresa não definida")
    return empresa_id


# =========================
# CRIAR EMPRESA (REGISTO)
# =========================
@router.post("/", response_model=EmpresaResponse)
def criar(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    # aqui NÃO usamos empresa_id porque ainda não existe empresa
    return crud.create_empresa(db, empresa)


# =========================
# LISTAR EMPRESAS (admin global)
# =========================
@router.get("/", response_model=list[EmpresaResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Empresa).all()


# =========================
# GET POR ID
# =========================
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obter(
    empresa_id: str,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa


# =========================
# UPDATE
# =========================
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar(
    empresa_id: str,
    dados: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)

    return empresa


# =========================
# DELETE
# =========================
@router.delete("/{empresa_id}")
def deletar(
    empresa_id: str,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()

    return {"message": "Empresa deletada com sucesso"}


# =========================
# ESTATÍSTICAS (GLOBAL SAAS)
# =========================
@router.get("/estatisticas/resumo")
def resumo(db: Session = Depends(get_db)):

    total = db.query(func.count(Empresa.id)).scalar()

    ativas = db.query(func.count(Empresa.id)).filter(
        Empresa.ativa == True
    ).scalar()

    inativas = db.query(func.count(Empresa.id)).filter(
        Empresa.ativa == False
    ).scalar()

    return {
        "total": total,
        "ativas": ativas,
        "inativas": inativas
    }