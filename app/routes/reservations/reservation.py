from fastapi import APIRouter, Depends, HTTPException
from ...controllers.reservaciones.reservation_controllers import (
    create_reservation, get_reservations_me, get_reservations_room, get_reservations_date, cancel_reservation, get_most_reserved_room, get_user_hours_this_month
)
from ...models.reservation.reservation import ReservationCreate
from ...routes.verificar.verifcar_admin import admin_required
from ...auth.dependencias import get_current_user
from sqlmodel import Session
from ...models.database.database import get_session

router = APIRouter(prefix="/reservations", tags=["Reservas"])

@router.post("/")
def create_new_reservation(reservation: ReservationCreate, user = Depends(get_current_user), db: Session = Depends(get_session)):
    return create_reservation(db, reservation, user["username"])

@router.get("/me")
def read_my_reservations(user = Depends(get_current_user), db: Session = Depends(get_session)):
    return get_reservations_me(db, user["username"])

@router.get("/room/{room_id}")
def read_reservations_room(room_id: int, db: Session = Depends(get_session)):
    return get_reservations_room(db, room_id)

@router.get("/date/{date}")
def read_reservations_date(date: str, db: Session = Depends(get_session)):
    return get_reservations_date(db, date)

@router.delete("/{reservation_id}")
def cancel_existing_reservation(reservation_id: int, user = Depends(get_current_user), db: Session = Depends(get_session)):
    return cancel_reservation(db, reservation_id, user["username"])

@router.get("/reports/most_reserved_room", dependencies=[Depends(admin_required)])
def report_most_reserved_room(db: Session = Depends(get_session)):
    return get_most_reserved_room(db)

@router.get("/reports/user_hours/{user_email}", dependencies=[Depends(admin_required)])
def report_user_hours(user_email: str, db: Session = Depends(get_session)):
    return get_user_hours_this_month(db, user_email)
