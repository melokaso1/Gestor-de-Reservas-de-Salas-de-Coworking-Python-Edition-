from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, time
from enum import Enum

class EstadoEnum(str, Enum):
    Pendiente = "Pendiente"
    Confirmada = "Confirmada"
    Cancelada = "Cancelada"

class Horario(SQLModel, table=True):
    __tablename__: str = "horario"
    id_horario: Optional[int] = Field(default=None, primary_key=True)
    hora_inicio: time
    hora_fin: time
    disponible: bool = Field(default=True)

class Reservation(SQLModel, table=True):
    __tablename__: str = "reservaciones"
    id_reservaciones: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    estado: EstadoEnum = Field(default=EstadoEnum.Pendiente)
    horario_id: int = Field(foreign_key="horario.id_horario")
    sede_id: int = Field(foreign_key="sedes.id_sede")
    usuarios_reservaciones: List["UsuarioReservacion"] = Relationship(back_populates="reservacion")
    salas_reservaciones: List["SalasReservacion"] = Relationship(back_populates="reservacion")

class UsuarioReservacion(SQLModel, table=True):
    __tablename__: str = "usuarios_reservaciones"
    reservaciones_id: int = Field(primary_key=True, foreign_key="reservaciones.id_reservaciones")
    user_id: int = Field(primary_key=True, foreign_key="usuarios.id_user")
    reservacion: Optional[Reservation] = Relationship(back_populates="usuarios_reservaciones")

class SalasReservacion(SQLModel, table=True):
    __tablename__: str = "salas_reservaciones"
    reservaciones_id: int = Field(primary_key=True, foreign_key="reservaciones.id_reservaciones")
    salas_id: int = Field(primary_key=True, foreign_key="salas.id_sala")
    reservacion: Optional[Reservation] = Relationship(back_populates="salas_reservaciones")

class ReservationCreate(SQLModel):
    sede_id: int
    sala_id: int
    fecha: date
    hora_inicio: str
    hora_fin: str

class ReservationRead(SQLModel):
    id_reservaciones: int
    fecha: date
    estado: EstadoEnum
    horario_id: int
    sede_id: int
