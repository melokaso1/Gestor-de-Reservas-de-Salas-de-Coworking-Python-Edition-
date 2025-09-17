from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.openapi.utils import get_openapi
from app.routes.usuario import user
from app.routes.rooms import room
from app.routes.reservations import reservation
from app.models.database.database import create_db_and_tables
from app.models.usuario.user import Usuarios
from app.models.room.room import Room
from app.models.reservation.reservation import Reservation, Horario, UsuarioReservacion, SalasReservacion

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origines, ajusta según sea necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user.router)
app.include_router(room.router)
app.include_router(reservation.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    class OAuth2PasswordBearerWithCookie(OAuth2):
        def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None, auto_error: bool = True): # type:ignore
            flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes or {}}) # type:ignore
            super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
    app.openapi_schema = get_openapi(
        title="API de Gestión de Reservaciones",
        version="1.0.0",
        description="API para gestionar usuarios, salas y reservaciones",
        routes=app.routes,
    )
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Gestión de Reservaciones!"}
