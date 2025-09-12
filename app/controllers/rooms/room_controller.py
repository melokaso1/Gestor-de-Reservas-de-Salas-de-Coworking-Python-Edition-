from fastapi import HTTPException
from sqlmodel import Session, select
from ...models.room.room import Room, RoomCreate, RoomRead

def create_room(db: Session, room_data: RoomCreate):
    room = Room(
        nombre=room_data.nombre,
        sede=room_data.sede,
        capacidad=room_data.capacidad,
        recursos=room_data.recursos
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_rooms(db: Session):
    return db.exec(select(Room)).all()

def get_room_by_id(db: Session, room_id: int):
    room = db.exec(select(Room).where(Room.id_room == room_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room

def update_room(db: Session, room_id: int, room_data: RoomCreate):
    room = db.exec(select(Room).where(Room.id_room == room_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    room.nombre = room_data.nombre
    room.sede = room_data.sede
    room.capacidad = room_data.capacidad
    room.recursos = room_data.recursos
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_id: int):
    room = db.exec(select(Room).where(Room.id_room == room_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    db.delete(room)
    db.commit()
    return {"message": "Sala eliminada"}
