from fastapi import FastAPI
from app.routes.usuario import user
from app.routes.rooms import room
from app.routes.reservations import reservation
from app.models.database.database import create_db_and_tables
from app.models.usuario.user import Usuarios
from app.models.room.room import Room
from app.models.reservation.reservation import Reservation, Horario, UsuarioReservacion, SalasReservacion

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(user.router)
app.include_router(room.router)
app.include_router(reservation.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Gestión de Reservaciones!"}
