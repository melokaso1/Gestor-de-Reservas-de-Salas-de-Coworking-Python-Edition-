from sqlmodel import Session, select
from fastapi import HTTPException
from ...models.room.room import Room, RoomCreate, RoomRead

def create_room(db: Session, room: RoomCreate):
    new_room = Room(
        nombre=room.nombre,
        capacidad=room.capacidad,
        descripcion=room.descripcion,
        precio=room.precio
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def get_rooms(db: Session):
    statement = select(Room)
    result = db.exec(statement)
    return result.all()

def get_room_by_id(db: Session, room_id: int):
    statement = select(Room).where(Room.id_sala == room_id)
    result = db.exec(statement)
    room = result.first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room

def update_room(db: Session, room_id: int, room_update: RoomCreate):
    statement = select(Room).where(Room.id_sala == room_id)
    result = db.exec(statement)
    room = result.first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    room.nombre = room_update.nombre
    room.capacidad = room_update.capacidad
    room.descripcion = room_update.descripcion
    room.precio = room_update.precio
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_id: int):
    statement = select(Room).where(Room.id_sala == room_id)
    result = db.exec(statement)
    room = result.first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    db.delete(room)
    db.commit()
    return room
