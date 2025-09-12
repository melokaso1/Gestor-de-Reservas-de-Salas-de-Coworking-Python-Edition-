from sqlmodel import Session, select
from fastapi import HTTPException
from ...models.reservation.reservation import Reservation, ReservationCreate, EstadoEnum, Horario, UsuarioReservacion, SalasReservacion
from ...models.room.room import Room
from ...models.usuario.user import Usuarios
from datetime import time
from sqlalchemy import func

def get_user_id_from_email(db: Session, email: str) -> int:
    statement = select(Usuarios).where(Usuarios.email == email)
    result = db.exec(statement)
    user = result.first()
    if not user:
        raise HTTPException(status_code=404, detail="❌Usuario no encontrado")
    return user.id_user

def create_reservation(db: Session, reservation: ReservationCreate, user_email: str):
    user_id = get_user_id_from_email(db, user_email)
    
    # Validate room exists
    statement = select(Room).where(Room.id_sala == reservation.sala_id)
    result = db.exec(statement)
    room = result.first()
    if not room:
        raise HTTPException(status_code=404, detail="❌Sala no encontrada")
    
    # Parse times
    try:
        hora_inicio = time.fromisoformat(reservation.hora_inicio)
        hora_fin = time.fromisoformat(reservation.hora_fin)
    except ValueError:
        raise HTTPException(status_code=400, detail="❌Formato de hora inválido. Use HH:MM:SS")
    
    # Validate 1-hour duration
    duration = (hora_fin.hour * 60 + hora_fin.minute) - (hora_inicio.hour * 60 + hora_inicio.minute)
    if duration != 60:
        raise HTTPException(status_code=400, detail="❌La reserva debe ser exactamente de 1 hora")
    
    # Find or create horario
    statement = select(Horario).where(Horario.hora_inicio == hora_inicio, Horario.hora_fin == hora_fin)
    horario = db.exec(statement).first()
    if not horario:
        horario = Horario(hora_inicio=hora_inicio, hora_fin=hora_fin)
        db.add(horario)
        db.commit()
        db.refresh(horario)
    
    # Check for overlaps
    # Query salas_reservaciones for sala_id, then get reservations with that horario_id and fecha
    statement = select(SalasReservacion).where(SalasReservacion.salas_id == reservation.sala_id)
    salas_res = db.exec(statement).all()
    reservaciones_ids = [sr.reservaciones_id for sr in salas_res]
    if reservaciones_ids:
        statement = select(Reservation).where(
            Reservation.id_reservaciones.in_(reservaciones_ids),
            Reservation.fecha == reservation.fecha,
            Reservation.estado != EstadoEnum.cancelada
        )
        existing_reservations = db.exec(statement).all()
        for res in existing_reservations:
            h = db.exec(select(Horario).where(Horario.id_horario == res.horario_id)).first()
            if h and (hora_inicio < h.hora_fin and hora_fin > h.hora_inicio):
                raise HTTPException(status_code=400, detail="❌Conflicto de horario con otra reserva")
    
    new_reservation = Reservation(
        fecha=reservation.fecha,
        estado=EstadoEnum.confirmada,
        horario_id=horario.id_horario
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    # Add to usuarios_reservaciones
    user_res = UsuarioReservacion(reservaciones_id=new_reservation.id_reservaciones, user_id=user_id)
    db.add(user_res)
    
    # Add to salas_reservaciones
    sala_res = SalasReservacion(reservaciones_id=new_reservation.id_reservaciones, salas_id=reservation.sala_id)
    db.add(sala_res)
    
    db.commit()
    return new_reservation

def get_reservations_me(db: Session, user_email: str):
    user_id = get_user_id_from_email(db, user_email)
    statement = select(UsuarioReservacion).where(UsuarioReservacion.user_id == user_id)
    user_res = db.exec(statement).all()
    reservaciones_ids = [ur.reservaciones_id for ur in user_res]
    if reservaciones_ids:
        statement = select(Reservation).where(Reservation.id_reservaciones.in_(reservaciones_ids))
        result = db.exec(statement)
        return result.all()
    return []

def get_reservations_room(db: Session, room_id: int):
    statement = select(SalasReservacion).where(SalasReservacion.salas_id == room_id)
    salas_res = db.exec(statement).all()
    reservaciones_ids = [sr.reservaciones_id for sr in salas_res]
    if reservaciones_ids:
        statement = select(Reservation).where(Reservation.id_reservaciones.in_(reservaciones_ids))
        result = db.exec(statement)
        return result.all()
    return []

def get_reservations_date(db: Session, date_str: str):
    from datetime import datetime
    try:
        fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="❌Formato de fecha inválido. Use YYYY-MM-DD")
    statement = select(Reservation).where(Reservation.fecha == fecha)
    result = db.exec(statement)
    return result.all()

def cancel_reservation(db: Session, reservation_id: int, user_email: str):
    user_id = get_user_id_from_email(db, user_email)
    # Check if user is associated
    statement = select(UsuarioReservacion).where(UsuarioReservacion.reservaciones_id == reservation_id, UsuarioReservacion.user_id == user_id)
    user_res = db.exec(statement).first()
    if not user_res:
        raise HTTPException(status_code=403, detail="❌No tienes permiso para cancelar esta reserva")
    statement = select(Reservation).where(Reservation.id_reservaciones == reservation_id)
    result = db.exec(statement)
    reservation = result.first()
    if not reservation:
        raise HTTPException(status_code=404, detail="❌Reserva no encontrada")
    reservation.estado = EstadoEnum.cancelada
    db.commit()
    db.refresh(reservation)
    return reservation

def get_most_reserved_room(db: Session):
    statement = select(SalasReservacion.salas_id, func.count(SalasReservacion.salas_id).label("count")).group_by(SalasReservacion.salas_id).order_by(func.count(SalasReservacion.salas_id).desc())
    result = db.exec(statement)
    most_reserved = result.first()
    if not most_reserved:
        return None
    return {"sala_id": most_reserved[0], "reservas": most_reserved[1]}

def get_user_hours_this_month(db: Session, user_email: str):
    from datetime import datetime
    user_id = get_user_id_from_email(db, user_email)
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    statement = select(UsuarioReservacion).where(UsuarioReservacion.user_id == user_id)
    user_res = db.exec(statement).all()
    reservaciones_ids = [ur.reservaciones_id for ur in user_res]
    if reservaciones_ids:
        statement = select(Reservation).where(
            Reservation.id_reservaciones.in_(reservaciones_ids),
            Reservation.fecha >= start_of_month.date(),
            Reservation.estado == EstadoEnum.confirmada
        )
        reservations = db.exec(statement).all()
        total_hours = len(reservations)  # Since each is 1 hour
        return {"usuario_id": user_id, "horas_este_mes": total_hours}
    return {"usuario_id": user_id, "horas_este_mes": 0}
