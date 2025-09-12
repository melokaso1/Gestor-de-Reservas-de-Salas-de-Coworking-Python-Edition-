from fastapi import APIRouter, Depends
from sqlmodel import Session
from ...models.database.database import get_session
from ...models.room.room import RoomCreate, RoomRead
from ...controllers.rooms.room_controller import create_room, get_rooms, get_room_by_id, update_room, delete_room
from ...routes.verificar.verifcar_admin import admin_required

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=list[RoomRead])
def read_rooms(db: Session = Depends(get_session)):
    return get_rooms(db)

@router.post("/", dependencies=[Depends(admin_required)], response_model=RoomRead)
def add_room(room: RoomCreate, db: Session = Depends(get_session)):
    return create_room(db, room)

@router.put("/{room_id}", dependencies=[Depends(admin_required)], response_model=RoomRead)
def edit_room(room_id: int, room: RoomCreate, db: Session = Depends(get_session)):
    return update_room(db, room_id, room)

@router.delete("/{room_id}", dependencies=[Depends(admin_required)])
def remove_room(room_id: int, db: Session = Depends(get_session)):
    return delete_room(db, room_id)
