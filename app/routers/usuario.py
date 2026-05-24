from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import verificar_senha, hash_senha

from app.models.usuario import Usuario, PapelUsuario

from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UpdateSenha
)

from app.crud import usuario as crud
from typing import Optional


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# =========================
# MULTI-TENANT
# =========================
def get_empresa_id(empresa_id: str = Cookie(None)):
    if not empresa_id:
        raise HTTPException(status_code=401, detail="Empresa não definida")
    return empresa_id


# =========================
# CRIAR USUÁRIO
# =========================
@router.post("/", response_model=UsuarioResponse)
def criar(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return crud.create_usuario(db, usuario, empresa_id)


# =========================
# LISTAR
# =========================
@router.get("/", response_model=list[UsuarioResponse])
def listar(
    search: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    papel: Optional[str] = None,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    return crud.get_usuarios(
        db,
        empresa_id,
        search,
        nome,
        email,
        papel
    )


# =========================
# GET POR ID
# =========================
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def pegar_por_id(
    usuario_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    usuario = crud.get_usuario_by_id(db, usuario_id, empresa_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# =========================
# UPDATE
# =========================
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar(
    usuario_id: str,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    atualizado = crud.update_usuario(db, usuario_id, usuario, empresa_id)

    if not atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return atualizado


# =========================
# DELETE
# =========================
@router.delete("/{usuario_id}")
def deletar(
    usuario_id: str,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):
    removido = crud.delete_usuario(db, usuario_id, empresa_id)

    if not removido:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"message": "Usuário deletado com sucesso"}


# =========================
# ESTATÍSTICAS
# =========================
@router.get("/estatisticas/resumo")
def resumo(
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    total = db.query(func.count(Usuario.id)).filter(
        Usuario.empresa_id == empresa_id
    ).scalar()

    admin = db.query(func.count(Usuario.id)).filter(
        Usuario.empresa_id == empresa_id,
        Usuario.papel == PapelUsuario.admin
    ).scalar()

    gerente = db.query(func.count(Usuario.id)).filter(
        Usuario.empresa_id == empresa_id,
        Usuario.papel == PapelUsuario.gerente
    ).scalar()

    return {
        "total": total,
        "admin": admin,
        "gerente": gerente
    }


# =========================
# ALTERAR SENHA
# =========================
@router.put("/{usuario_id}/alterar-senha")
def alterar_senha(
    usuario_id: str,
    dados: UpdateSenha,
    db: Session = Depends(get_db),
    empresa_id: str = Depends(get_empresa_id)
):

    usuario = crud.get_usuario_by_id(db, usuario_id, empresa_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    senha_correta = verificar_senha(dados.senha_atual, usuario.senha)

    if not senha_correta:
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    usuario.senha = hash_senha(dados.nova_senha)

    db.commit()

    return {"mensagem": "Senha alterada com sucesso"}








# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.security import verificar_senha,  hash_senha

# from sqlalchemy import func

# from app.models.usuario import Usuario, PapelUsuario

# from app.core.database import get_db

# from app.schemas.usuario import (
#     UsuarioCreate,
#     UsuarioUpdate,
#     UsuarioResponse,
#     UpdateSenha
# )

# from app.crud import usuario as crud
# from typing import Optional


# router = APIRouter(
#     prefix="/usuarios",
#     tags=["Usuarios"]
# )


# @router.post("/", response_model=UsuarioResponse)
# def criar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
#     return crud.create_usuario(db, usuario)


# @router.get("/", response_model=list[UsuarioResponse])
# def listar(
#     search: Optional[str] = None,
#     nome: Optional[str] = None,
#     email: Optional[str] = None,
#     papel: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     return crud.get_usuarios(
#         db,
#         search,
#         nome,
#         email,
#         papel
#     )






# @router.get("/{usuario_id}", response_model=UsuarioResponse)
# def pegar_por_id(usuario_id: str, db: Session = Depends(get_db)):
#     usuario = crud.get_usuario_by_id(db, usuario_id)

#     if not usuario:
#         raise HTTPException(
#             status_code=404,
#             detail="Usuário não encontrado"
#         )

#     return usuario


# @router.put("/{usuario_id}", response_model=UsuarioResponse)
# def atualizar(
#     usuario_id: str,
#     usuario: UsuarioUpdate,
#     db: Session = Depends(get_db)
# ):
#     usuario_db = crud.update_usuario(
#         db,
#         usuario_id,
#         usuario
#     )

#     if not usuario_db:
#         raise HTTPException(
#             status_code=404,
#             detail="Usuário não encontrado"
#         )

#     return usuario_db


# @router.delete("/{usuario_id}")
# def deletar(usuario_id: str, db: Session = Depends(get_db)):
#     usuario = crud.delete_usuario(db, usuario_id)

#     if not usuario:
#         raise HTTPException(
#             status_code=404,
#             detail="Usuário não encontrado"
#         )

#     return {"message": "Usuário deletado com sucesso"}


# @router.get("/estatisticas/resumo")
# def resumo_veiculos(db: Session = Depends(get_db)):

#     total = db.query(func.count(Usuario.id)).scalar()

#     admin = db.query(func.count(Usuario.id)).filter(
#         Usuario.papel == PapelUsuario.admin
#     ).scalar()

#     gerente = db.query(func.count(Usuario.id)).filter(
#         Usuario.papel == PapelUsuario.gerente
#     ).scalar()


#     return {
#         "total": total,
#         "admin": admin,
#         "gerente": gerente,
#     }



# @router.put("/{usuario_id}/alterar-senha")
# def alterar_senha(
#     usuario_id: str,
#     dados: UpdateSenha,
#     db: Session = Depends(get_db)
# ):

#     usuario = crud.get_usuario_by_id(
#         db,
#         usuario_id
#     )

#     if not usuario:
#         raise HTTPException(
#             status_code=404,
#             detail="Usuário não encontrado"
#         )

#     senha_correta = verificar_senha(
#         dados.senha_atual,
#         usuario.senha
#     )

#     if not senha_correta:
#         raise HTTPException(
#             status_code=400,
#             detail="Senha atual incorreta"
#         )

#     usuario.senha = hash_senha(
#         dados.nova_senha
#     )

#     db.commit()

#     return {
#         "mensagem": "Senha alterada com sucesso"
#     }
