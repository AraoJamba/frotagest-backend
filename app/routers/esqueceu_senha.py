from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema
from app.core.config_email import conf
from app.core.security import criar_token_reset
from jose import jwt, JWTError

router = APIRouter()

@router.post("/esqueceu-senha")
async def esqueceu_senha(email: str):

    token = criar_token_reset(email)

    link = f"http://localhost:3000/resetar-senha?token={token}"

    message = MessageSchema(
        subject="Recuperação de senha",
        recipients=[email],
        body=f"""
        Clique no link para redefinir sua senha:

        {link}
        """,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"msg": "Email enviado"}




@router.post("/resetar-senha")
async def resetar_senha(token: str, nova_senha: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

    except JWTError:
        return {"erro": "Token inválido"}

    # 🔥 aqui você atualiza no banco
    # hash da senha etc

    return {"msg": "Senha atualizada"}