from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.usuario.user import Usuarios
from sqlalchemy import func

def create_user(db: Session, user: Usuarios):
    if not all ([user.nombre, user.email, user.contraseña]):
        raise HTTPException(status_code=400, detail="❌Faltan datos obligatorios.")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session):
    statement = select(Usuarios)
    result = db.exec(statement)
    return result.all()

def get_user_by_id(db: Session, user_id: int):
    statement = select(Usuarios).where(Usuarios.id_user == user_id)
    result = db.exec(statement)
    return result.first()

def get_user_by_email(db: Session, email: str):
    statement = select(Usuarios).where(func.lower(Usuarios.email) == func.lower(email))
    result = db.exec(statement)
    return result.first()

def delete_user(db: Session, user_id: int):
    statement = select(Usuarios).where(Usuarios.id_user == user_id)
    result = db.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return user
