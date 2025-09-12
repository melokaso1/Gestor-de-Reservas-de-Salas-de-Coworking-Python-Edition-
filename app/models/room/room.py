from sqlmodel import SQLModel, Field
from typing import Optional

class Room(SQLModel, table=True):
    __tablename__ = "salas"
    id_sala: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    capacidad: int
    descripcion: str
    precio: float

class RoomCreate(SQLModel):
    nombre: str
    capacidad: int
    descripcion: str
    precio: float

class RoomRead(SQLModel):
    id_sala: int
    nombre: str
    capacidad: int
    descripcion: str
    precio: float
