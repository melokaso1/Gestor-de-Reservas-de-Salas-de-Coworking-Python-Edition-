from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import date, time, timedelta
from ...models.reservation.reservation import Reservation, EstadoEnum, ReservationCreate, ReservationRead
from ...models.usuario.user import Usuarios
from ...models.room.room import Room

def create_reservation(db: Session, reservation_data: ReservationCreate, user_id: int):
    # Validar que la sala existe
    room = db.exec(select(Room).where(Room.id_room == reservation_data.sala_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    # Validar que la reserva sea de 1 hora exacta
    duration = (reservation_data.hora_fin.hour * 60 + reservation_data.hora_fin.minute) - (reservation_data.hora_inicio.hour * 60 + reservation_data.hora_inicio.minute)
    if duration != 60:
        raise HTTPException(status_code=400, detail="La reserva debe ser exactamente de 1 hora")

    # Validar que no haya cruce de horarios para la misma sala en la misma fecha
    overlapping = db.exec(
        select(Reservation).where(
            Reservation.sala_id == reservation_data.sala_id,
            Reservation.fecha == reservation_data.fecha,
            Reservation.estado != EstadoEnum.cancelada,
            ((Reservation.hora_inicio < reservation_data.hora_fin) & (Reservation.hora_fin > reservation_data.hora_inicio))
        )
    ).first()
    if overlapping:
        raise HTTPException(status_code=409, detail="Ya existe una reserva en ese horario para esta sala")

    # Crear la reserva
    reservation = Reservation(
        usuario_id=user_id,
        sala_id=reservation_data.sala_id,
        fecha=reservation_data.fecha,
        hora_inicio=reservation_data.hora_inicio,
        hora_fin=reservation_data.hora_fin,
        estado=EstadoEnum.confirmada
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def get_reservations_me(db: Session, user_id: int):
    return db.exec(select(Reservation).where(Reservation.usuario_id == user_id)).all()

def get_reservations_room(db: Session, room_id: int):
    return db.exec(select(Reservation).where(Reservation.sala_id == room_id)).all()

def get_reservations_date(db: Session, date_str: str):
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
    return db.exec(select(Reservation).where(Reservation.fecha == target_date)).all()

def cancel_reservation(db: Session, reservation_id: int, user_id: int):
    reservation = db.exec(select(Reservation).where(Reservation.id_reservaciones == reservation_id)).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if reservation.usuario_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva")
    reservation.estado = EstadoEnum.cancelada
    db.commit()
    db.refresh(reservation)
    return reservation

