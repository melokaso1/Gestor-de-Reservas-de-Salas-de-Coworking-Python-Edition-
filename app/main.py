from fastapi import FastAPI
from app.routes.usuario import user
from app.models.database.database import create_db_and_tables


app = FastAPI()

app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Gestión de Reservaciones!"}

