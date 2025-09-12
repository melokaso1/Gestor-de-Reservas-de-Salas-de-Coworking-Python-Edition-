from passlib.context import CryptContext

contexto_clave = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_contraseña(contraseña: str) -> str:
    return contexto_clave.hash(contraseña)

def verificar_contraseña(contraseña: str, contraseña_hash: str) -> bool:
    return contexto_clave.verify(contraseña, contraseña_hash)
