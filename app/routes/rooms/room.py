from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...models.room.room import Room, RoomCreate
from ...controllers.rooms.room_controller import create_room, get_rooms, get_room_by_id, update_room, delete_room
from ...auth.dependencias import get_current_user
from ...routes.verificar.verifcar_admin import admin_required
from ...models.database.database import get_session

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/")
def read_rooms(db: Session = Depends(get_session), user=Depends(get_current_user)):
    return get_rooms(db)

@router.post("/", dependencies=[Depends(admin_required)])
def add_room(room: RoomCreate, db: Session = Depends(get_session)):
    return create_room(db, room)

@router.put("/{room_id}", dependencies=[Depends(admin_required)])
def modify_room(room_id: int, room: RoomCreate, db: Session = Depends(get_session)):
    return update_room(db, room_id, room)

@router.delete("/{room_id}", dependencies=[Depends(admin_required)])
def remove_room(room_id: int, db: Session = Depends(get_session)):
    return delete_room(db, room_id)
