from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.autenticar_contraseña import hash_contraseña, verificar_contraseña
from app.auth.jwt_hand import crear_token
from app.models.usuario.user import Usuarios, UsuarioCreate, RolEnum
from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Session, select
from ...models.database.database import get_session
from ...controllers.usuarios.user_controller import create_user, get_user, get_user_by_id, delete_user
from ...auth.dependencias import get_current_user
from ..verificar.verifcar_admin import admin_required

router = APIRouter(prefix="/usuario", tags=["Usuarios"])

class UserCreateSchema(BaseModel):
    nombre: str
    email: str
    rol: str
    password: str

@router.post("/registro_usuario")
def registrar_usuario(user: UserCreateSchema, db: Session = Depends(get_session)):
    user.email = user.email.lower()
    aparece = select(Usuarios).where(func.lower(Usuarios.email) == user.email)
    resultado = db.exec(aparece).first()

    if resultado:
        raise HTTPException(status_code=400, detail="❌El email ya está registrado.")
    hashed_password = hash_contraseña(user.password)
    print(f"Hashed password: {hashed_password}")  # Log hash para depuración

    if user.rol == "Admin":
        rol = RolEnum.Admin
    else:
        rol = RolEnum.User

    new_user = Usuarios(
        nombre=user.nombre,
        email=user.email,
        rol=rol,
        contraseña=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    print(f"Login attempt with username: {form_data.username}, password: {form_data.password}")
    usuario = db.exec(select(Usuarios).where(Usuarios.email == form_data.username.lower())).first()
    if not usuario:
        print(f"Usuario no encontrado para email: {form_data.username.lower()}")
        raise HTTPException(status_code=401, detail="❌Credenciales inválidas.")
    print(f"Usuario encontrado: {usuario.email}")
    print(f"Stored hash for {usuario.email}: {usuario.contraseña}")
    password_check = verificar_contraseña(form_data.password, usuario.contraseña)
    print(f"Resultado de verificar_contraseña: {password_check}")
    if not password_check:
        print(f"Contraseña incorrecta para usuario: {usuario.email}")
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
