from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha_normal: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_normal, senha_hash)





SECRET_KEY = "3ec4e0be-bc87-4255-b788-267766523ef1"
ALGORITHM = "HS256"

def criar_token_reset(email: str):
    exp = datetime.utcnow() + timedelta(minutes=30)
    data = {"sub": email, "exp": exp}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)











# from passlib.context import CryptContext

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )

# def hash_senha(senha: str):
#     return pwd_context.hash(senha)

# def verificar_senha(
#     senha_normal: str,
#     senha_hash: str
# ):
#     return pwd_context.verify(
#         senha_normal,
#         senha_hash
# )