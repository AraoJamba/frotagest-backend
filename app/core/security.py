from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(
    senha_normal: str,
    senha_hash: str
):
    return pwd_context.verify(
        senha_normal,
        senha_hash
)