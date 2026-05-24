from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.usuario import Usuario, PapelUsuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_senha


# =========================
# CREATE (TENANT SAFE)
# =========================
def create_usuario(db: Session, usuario: UsuarioCreate, empresa_id: str):
    
    # valida email duplicado por empresa
    email_existe = db.query(Usuario).filter(
        Usuario.email == usuario.email,
        Usuario.empresa_id == empresa_id
    ).first()

    if email_existe:
        raise Exception("Já existe um usuário com este email nesta empresa")

    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha),
        papel=usuario.papel,
        empresa_id=empresa_id
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# =========================
# LISTAR (TENANT SAFE)
# =========================
def get_usuarios(
    db: Session,
    empresa_id: str,
    search: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    papel: Optional[str] = None
):
    query = db.query(Usuario).filter(
        Usuario.empresa_id == empresa_id
    )

    if search:
        query = query.filter(
            or_(
                Usuario.nome.contains(search),
                Usuario.email.contains(search),
                Usuario.papel.contains(search)
            )
        )

    if nome:
        query = query.filter(Usuario.nome.contains(nome))

    if email:
        query = query.filter(Usuario.email.contains(email))

    if papel:
        query = query.filter(Usuario.papel == papel)

    return query.all()


# =========================
# GET POR ID (TENANT SAFE)
# =========================
def get_usuario_by_id(db: Session, usuario_id: str, empresa_id: str):
    return db.query(Usuario).filter(
        Usuario.id == usuario_id,
        Usuario.empresa_id == empresa_id
    ).first()


# =========================
# GET POR e-MAIL (TENANT SAFE)
# =========================
def buscar_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


# =========================
# UPDATE (TENANT SAFE)
# =========================
def update_usuario(
    db: Session,
    usuario_id: str,
    usuario: UsuarioUpdate,
    empresa_id: str
):
    db_usuario = get_usuario_by_id(db, usuario_id, empresa_id)

    if not db_usuario:
        return None

    # valida email duplicado
    if usuario.email:
        email_existe = db.query(Usuario).filter(
            Usuario.email == usuario.email,
            Usuario.empresa_id == empresa_id,
            Usuario.id != usuario_id
        ).first()

        if email_existe:
            raise Exception("Email já existe nesta empresa")

    if usuario.nome is not None:
        db_usuario.nome = usuario.nome

    if usuario.email is not None:
        db_usuario.email = usuario.email

    if usuario.senha is not None:
        db_usuario.senha = hash_senha(usuario.senha)

    if usuario.papel is not None:
        db_usuario.papel = usuario.papel

    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# =========================
# DELETE (TENANT SAFE)
# =========================
def delete_usuario(db: Session, usuario_id: str, empresa_id: str):
    db_usuario = get_usuario_by_id(db, usuario_id, empresa_id)

    if not db_usuario:
        return None

    db.delete(db_usuario)
    db.commit()

    return db_usuario












# from sqlalchemy.orm import Session
# from app.models.usuario import Usuario
# from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
# from app.core.security import hash_senha

# from passlib.context import CryptContext

# from sqlalchemy import or_
# from typing import Optional


# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# def create_usuario(db: Session, usuario: UsuarioCreate):
#     db_usuario = Usuario(
#         nome=usuario.nome,
#         email=usuario.email,
#         senha=hash_senha(usuario.senha),
#         papel=usuario.papel
#     )

#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)

#     return db_usuario


# def get_usuarios(
#     db: Session,
#     search: Optional[str] = None,
#     nome: Optional[str] = None,
#     email: Optional[str] = None,
#     papel: Optional[str] = None
# ):
#     query = db.query(Usuario)

#     # Pesquisa geral
#     if search:
#         query = query.filter(
#             or_(
#                 Usuario.nome.contains(search),
#                 Usuario.email.contains(search),
#                 Usuario.papel.contains(search)
#             )
#         )

#     # Filtros específicos
#     if nome:
#         query = query.filter(Usuario.nome.contains(nome))

#     if email:
#         query = query.filter(Usuario.email.contains(email))

#     if papel:
#         query = query.filter(Usuario.papel == papel)

#     return query.all()



# def get_usuario_by_id(db: Session, usuario_id: str):
#     return db.query(Usuario).filter(
#         Usuario.id == usuario_id
#     ).first()


# def update_usuario(
#     db: Session,
#     usuario_id: str,
#     usuario: UsuarioUpdate
# ):
#     db_usuario = get_usuario_by_id(db, usuario_id)

#     if db_usuario:

#         if usuario.nome is not None:
#             db_usuario.nome = usuario.nome

#         if usuario.email is not None:
#             db_usuario.email = usuario.email

#         if usuario.senha is not None:
#             db_usuario.senha = hash_senha(usuario.senha)

#         if usuario.papel is not None:
#             db_usuario.papel = usuario.papel

#         db.commit()
#         db.refresh(db_usuario)

#     return db_usuario


# def delete_usuario(db: Session, usuario_id: str):
#     db_usuario = get_usuario_by_id(db, usuario_id)

#     if db_usuario:
#         db.delete(db_usuario)
#         db.commit()

#     return db_usuario

