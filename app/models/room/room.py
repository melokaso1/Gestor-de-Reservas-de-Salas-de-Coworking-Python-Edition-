from sqlmodel import SQLModel, Field
from typing import Optional

class Sede(SQLModel, table=True):
    __tablename__ = "sedes"# type:ignore
    id_sede: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class SedesSalas(SQLModel, table=True):
    __tablename__ = "sedes_salas"# type:ignore
    sedes_id: int = Field(primary_key=True, foreign_key="sedes.id_sede")
    salas_id: int = Field(primary_key=True, foreign_key="salas.id_sala")

class Room(SQLModel, table=True):
    __tablename__ = "salas"# type:ignore
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
    sede_id: Optional[int] = None

class RoomRead(SQLModel):
    id_sala: int
    nombre: str
    capacidad: int
    descripcion: str
    precio: float
    sede_id: Optional[int]
