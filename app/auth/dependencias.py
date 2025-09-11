from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth.jwt_hand import SECRET_KEY, ALGORITHM


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        rol = payload.get("rol")
        if username is None or rol is None:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return {"username": username, "rol": rol}
    except JWTError:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
