from sqlmodel import Session
from fastapi import HTTPException
from ...models.usuario.user import Usuarios

def create_user(db: Session, user: Usuarios):
    if not all ([user.id_user, user.nombre, user.email, user.contraseña]):
        raise HTTPException(status_code=400, detail="❌Faltan datos obligatorios.")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session):
    return db.query(Usuarios).all()

from sqlmodel import select

def get_user_by_id(db: Session, user_id: int):
    statement = select(Usuarios).where(Usuarios.id_user == user_id)
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


