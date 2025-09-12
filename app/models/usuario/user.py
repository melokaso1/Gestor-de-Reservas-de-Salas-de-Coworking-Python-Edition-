from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RolEnum(str, Enum):
    admin = "Admin"
    user = "User"

class Usuarios(SQLModel, table=True):
    id_user: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    rol: RolEnum = Field(default=RolEnum.user)
    contraseña: str
    
class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    rol: Optional[str] = "User"
    password: str

class UsuarioRead(SQLModel):
    id_user: int
    nombre: str
    email: str
    rol: RolEnum

