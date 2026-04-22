from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

from passlib.context import CryptContext

from sqlalchemy import or_
from typing import Optional


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str):
    return pwd_context.hash(senha)


def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha),
        papel=usuario.papel
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


def get_usuarios(
    db: Session,
    search: Optional[str] = None,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    papel: Optional[str] = None
):
    query = db.query(Usuario)

    # Pesquisa geral
    if search:
        query = query.filter(
            or_(
                Usuario.nome.contains(search),
                Usuario.email.contains(search),
                Usuario.papel.contains(search)
            )
        )

    # Filtros específicos
    if nome:
        query = query.filter(Usuario.nome.contains(nome))

    if email:
        query = query.filter(Usuario.email.contains(email))

    if papel:
        query = query.filter(Usuario.papel == papel)

    return query.all()



def get_usuario_by_id(db: Session, usuario_id: str):
    return db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()


def update_usuario(
    db: Session,
    usuario_id: str,
    usuario: UsuarioUpdate
):
    db_usuario = get_usuario_by_id(db, usuario_id)

    if db_usuario:
        db_usuario.nome = usuario.nome
        db_usuario.email = usuario.email
        db_usuario.senha = hash_senha(usuario.senha)
        db_usuario.papel = usuario.papel

        db.commit()
        db.refresh(db_usuario)

    return db_usuario


def delete_usuario(db: Session, usuario_id: str):
    db_usuario = get_usuario_by_id(db, usuario_id)

    if db_usuario:
        db.delete(db_usuario)
        db.commit()

    return db_usuario
