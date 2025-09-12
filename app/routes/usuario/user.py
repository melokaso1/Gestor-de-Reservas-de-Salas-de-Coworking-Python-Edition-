from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ...auth.autenticar_contraseña import hash_contraseña, verificar_contraseña
from ...auth.jwt_hand import crear_token
from ...models.usuario.user import Usuarios, UsuarioCreate, RolEnum
from pydantic import BaseModel, Field
from typing import Optional

class UserCreateSchema(BaseModel):
    nombre: str = Field(..., example="Juan Perez")
    email: str = Field(..., example="juan@example.com")
    rol: str = Field("User", example="User")
    password: str = Field(..., example="password123")
from ..verificar.verifcar_admin import admin_required
from sqlmodel import Session, select
from ...models.database.database import get_session
from ...controllers.usuarios.user_controller import create_user, get_user, get_user_by_id, delete_user
from ...auth.dependencias import get_current_user

router = APIRouter(prefix="/usuario", tags=["Usuarios"])

@router.post("/test")
def test_endpoint():
    return {"message": "Test endpoint works"}

@router.post("/test_user")
def test_user_endpoint(user: UserCreateSchema):
    return {"received": user.dict()}

@router.post("/registro_usuario")
def registrar_usuario(user: UserCreateSchema, db: Session = Depends(get_session)):
    aparece =  select(Usuarios).where(Usuarios.email == user.email)

    resultado = db.exec(aparece).first()

    if resultado:
        raise HTTPException(status_code=400, detail="❌El email ya está registrado.")
    hashed_password = hash_contraseña(user.password)

    # Convertir rol string a RolEnum
    if user.rol == "Admin":
        rol = RolEnum.admin
    else:
        rol = RolEnum.user

    new_user = Usuarios(
        nombre = user.nombre,
        email = user.email,
        rol = rol,
        contraseña = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    usuario = db.exec(select(Usuarios).where(Usuarios.email == form_data.username)).first()
    if not usuario or not verificar_contraseña(form_data.password, usuario.contraseña):
        raise HTTPException(status_code=401, detail="❌Credenciales inválidas.")
    
    token = crear_token({"username": usuario.email, "rol": usuario.rol.value})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/usuario_actual")
def get_usuario_actual(user = Depends(get_current_user)):
    return user

@router.get("/todo", dependencies=[Depends(admin_required)])
def leer_usuarios(db: Session = Depends(get_session)):
    return get_user(db)

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
def eliminar_usuario(user_id: int, db: Session = Depends(get_session)):
    return delete_user(db, user_id)