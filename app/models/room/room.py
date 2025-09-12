from sqlmodel import SQLModel, Field
from typing import Optional, List

class Room(SQLModel, table=True):
    id_room: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    sede: str
    capacidad: int
    recursos: str  # Lista de recursos como string, e.g., "pizarra,proyector"

class RoomCreate(SQLModel):
    nombre: str
    sede: str
    capacidad: int
    recursos: str

class RoomRead(SQLModel):
    id_room: int
    nombre: str
    sede: str
    capacidad: int
    recursos: str
