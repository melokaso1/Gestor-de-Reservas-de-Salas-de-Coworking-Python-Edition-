from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt_hand import verify_token
from app.controllers.usuarios.user_controller import get_user_by_email
from app.models.database.database import get_session
from sqlmodel import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuario/login", auto_error=True)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email = payload.get("username")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(db, email.lower())
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
