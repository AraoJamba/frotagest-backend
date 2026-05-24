from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
import bcrypt

from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginSchema
from app.schemas.usuario import PapelUsuario


from app.schemas.auth import RegistroEmpresaAdmin
from app.models.empresa import Empresa
from app.core.security import hash_senha, SECRET_KEY, ALGORITHM


from fastapi_mail import FastMail, MessageSchema
from app.core.config_email import conf

from app.core.security import criar_token_reset
from jose import jwt, JWTError


from pydantic import BaseModel, EmailStr


from app.core.database import get_db

from app.crud import usuario as crud


from passlib.context import CryptContext




router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



@router.post("/registro")
def registrar_empresa_admin(dados: RegistroEmpresaAdmin, db: Session = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(
        Usuario.email == dados.usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Já existe um utilizador com este email")

    empresa_existente = db.query(Empresa).filter(
        Empresa.nif == dados.empresa.nif
    ).first()

    if empresa_existente:
        raise HTTPException(status_code=400, detail="Já existe uma empresa com esse NIF")

    empresa = Empresa(
        nome=dados.empresa.nome,
        nif=dados.empresa.nif,
        telefone=dados.empresa.telefone,
        email=dados.empresa.email,
        endereco=dados.empresa.endereco
    )

    db.add(empresa)
    db.flush()  # gera ID

    senha_hash = hash_senha(dados.usuario.senha)

    usuario = Usuario(
        nome=dados.usuario.nome,
        email=dados.usuario.email,
        senha=senha_hash,
        papel=PapelUsuario.admin,  # fixo aqui
        empresa_id=empresa.id
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {
        "message": "Empresa e admin criados com sucesso",
        "empresa_id": empresa.id,
        "usuario_id": usuario.id
    }


@router.post("/login")
def login(dados: LoginSchema, response: Response, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    senha_valida = bcrypt.checkpw(
        dados.senha.encode(),
        usuario.senha.encode()
    )

    if not senha_valida:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    # cookies (multi-tenant básico)
    response.set_cookie(
        key="access_token",
        value=str(usuario.id),
        httponly=True,
        secure=False,
        samesite="lax"
    )

    response.set_cookie(
        key="empresa_id",
        value=str(usuario.empresa_id),
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {
        "message": "Login realizado com sucesso",
        "usuario_id": usuario.id,
        "empresa_id": usuario.empresa_id
    }


@router.get("/eu")
def me(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):

    if not access_token:
        raise HTTPException(status_code=401, detail="Não autenticado")

    usuario = db.query(Usuario).filter(
        Usuario.id == access_token
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "papel": usuario.papel,
        "empresa_id": usuario.empresa_id
    }




from pydantic import BaseModel, EmailStr

class EsqueceuSenhaRequest(BaseModel):
    email: EmailStr

@router.post("/esqueceu-senha")
async def esqueceu_senha(
    data: EsqueceuSenhaRequest,
    db: Session = Depends(get_db)
):
    email = data.email

    usuario = crud.buscar_usuario_por_email(db, email)

    if usuario:
        token = criar_token_reset(email)

        link = f"http://localhost:3000/resetar-senha?token={token}"

        message = MessageSchema(
            subject="Recuperação de senha",
            recipients=[email],
            body=f"Link: {link}",
            subtype="plain"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    return {"msg": "Se o email existir, você receberá um link de recuperação"}




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ResetSenhaRequest(BaseModel):
    token: str
    nova_senha: str

@router.post("/resetar-senha")
async def resetar_senha(
    data: ResetSenhaRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

    except JWTError:
        return {"erro": "Token inválido"}

    # 🔍 Buscar usuário
    usuario = crud.buscar_usuario_por_email(db, email)

    if not usuario:
        return {"erro": "Usuário não encontrado"}

    # 🔐 HASH DA NOVA SENHA
    senha_hash = pwd_context.hash(data.nova_senha)

    # 💾 Atualizar no banco
    usuario.senha = senha_hash

    db.commit()

    return {"msg": "Senha atualizada com sucesso"}



# @router.post("/esqueceu-senha")
# async def esqueceu_senha(data: EsqueceuSenhaRequest):

#     email = data.email

#     token = criar_token_reset(email)

#     link = f"http://localhost:3000/resetar-senha?token={token}"

#     message = MessageSchema(
#         subject="Recuperação de senha",
#         recipients=[email],
#         body=f"""
#             <h2>Recuperação de senha</h2>
#             <p>Clique no botão abaixo:</p>
#             <a href="{link}">Redefinir senha</a>
#         """,
#         subtype="html"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)

#     return {"msg": "Email enviado"}



# @router.post("/esqueceu-senha")
# async def esqueceu_senha(email: str):

#     token = criar_token_reset(email)

#     link = f"http://localhost:3000/resetar-senha?token={token}"

#     message = MessageSchema(
#         subject="Recuperação de senha",
#         recipients=[email],
#         body=f"""
#         Clique no link para redefinir sua senha:

#         {link}
#         """,
#         subtype="plain"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)

#     return {"msg": "Email enviado"}






# @router.post("/resetar-senha")
# async def resetar_senha(token: str, nova_senha: str):

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")

#     except JWTError:
#         return {"erro": "Token inválido"}

#     # 🔥 aqui você atualiza no banco
#     # hash da senha etc

#     return {"msg": "Senha atualizada"}










# from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
# from sqlalchemy.orm import Session
# import bcrypt

# from app.core.database import get_db
# from app.models.usuario import Usuario
# from app.schemas.auth import LoginSchema

# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"]
# )


# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"]
# )



# @router.post("/login")
# def login(dados: LoginSchema, response: Response, db: Session = Depends(get_db)):
#     usuario = db.query(Usuario).filter(
#         Usuario.email == dados.email
#     ).first()

#     if not usuario:
#         raise HTTPException(status_code=400, detail="Credenciais inválidas")

#     senha_valida = bcrypt.checkpw(
#         dados.senha.encode(),
#         usuario.senha.encode()
#     )

#     if not senha_valida:
#         raise HTTPException(status_code=400, detail="Credenciais inválidas")

#     response.set_cookie(
#         key="access_token",
#         value=str(usuario.id),
#         httponly=True,
#         secure=False,
#         samesite="lax"
#     )

#     response.set_cookie(
#         key="empresa_id",
#         value=str(usuario.empresa_id),
#         httponly=True,
#         secure=False,
#         samesite="lax"
#     )

#     return {"message": "Login realizado com sucesso"}


# @router.get("/eu")
# def me(
#     access_token: str = Cookie(None),
#     db: Session = Depends(get_db)
# ):
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Não autenticado")

#     usuario = db.query(Usuario).filter(
#         Usuario.id == access_token
#     ).first()

#     if not usuario:
#         raise HTTPException(status_code=401, detail="Usuário inválido")

#     return {
#         "id": usuario.id,
#         "nome": usuario.nome,
#         "email": usuario.email,
#         "papel": usuario.papel,
#         "empresa_id": usuario.empresa_id
#     }




# @router.get("/eu")
# def me(
#     access_token: str = Cookie(None),
#     db: Session = Depends(get_db)
# ):
#     if not access_token:
#         raise HTTPException(
#             status_code=401,
#             detail="Não autenticado"
#         )

#     usuario = db.query(Usuario).filter(
#         Usuario.id == access_token
#     ).first()

#     if not usuario:
#         raise HTTPException(
#             status_code=401,
#             detail="Usuário inválido"
#         )

#     return {
#         "id": usuario.id,
#         "nome": usuario.nome,
#         "email": usuario.email,
#         "papel": usuario.papel
#     }


# @router.post("/login")
# def login(
#     dados: LoginSchema,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     usuario = db.query(Usuario).filter(
#         Usuario.email == dados.email
#     ).first()

#     if not usuario:
#         raise HTTPException(status_code=400, detail="Credenciais inválidas")

#     senha_valida = bcrypt.checkpw(
#         dados.senha.encode(),
#         usuario.senha.encode()
#     )

#     if not senha_valida:
#         raise HTTPException(status_code=400, detail="Credenciais inválidas")

#     # Criar cookie
#     response.set_cookie(
#         key="access_token",
#         value=str(usuario.id),
#         httponly=True,
#         secure=False,  # True em produção
#         samesite="lax"
#     )

#     return {"message": "Login realizado com sucesso"}
