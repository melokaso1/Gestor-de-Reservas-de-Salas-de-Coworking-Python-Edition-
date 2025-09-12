from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time
from enum import Enum

class EstadoEnum(str, Enum):
    pendiente = "Pendiente"
    confirmada = "Confirmada"
    cancelada = "Cancelada"

class Reservation(SQLModel, table=True):
    id_reservaciones: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id_user")
    sala_id: int = Field(foreign_key="room.id_room")
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: EstadoEnum = Field(default=EstadoEnum.pendiente)

class ReservationCreate(SQLModel):
    sala_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time

class ReservationRead(SQLModel):
    id_reservaciones: int
    usuario_id: int
    sala_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: EstadoEnum
    
