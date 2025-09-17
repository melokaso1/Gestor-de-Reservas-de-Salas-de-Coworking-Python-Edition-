from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.reservation.reservation import Reservation, ReservationCreate, EstadoEnum, Horario, UsuarioReservacion, SalasReservacion
from app.models.room.room import Room, Sede, SedesSalas
from app.models.usuario.user import Usuarios
from datetime import time, datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def get_user_id_from_email(db: Session, email: str) -> int:
    statement = select(Usuarios).where(Usuarios.email == email)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌Usuario no encontrado")
    if user.id_user is None:
        raise HTTPException(status_code=500, detail="❌El usuario no tiene un ID válido")
    return user.id_user 

def create_reservation(db: Session, reservation: ReservationCreate, user_email: str):
    user_id = get_user_id_from_email(db, user_email)

    # Validar que la sede existe
    sede = db.exec(select(Sede).where(Sede.id_sede == reservation.sede_id)).first()
    if not sede:
        raise HTTPException(status_code=404, detail="❌Sede no encontrada")

    # Validar que la sala existe
    room = db.exec(select(Room).where(Room.id_sala == reservation.sala_id)).first()
    if not room:
        raise HTTPException(status_code=404, detail="❌Sala no encontrada")
    
    # Parsear horas
    try:
        hora_inicio = time.fromisoformat(reservation.hora_inicio)
        hora_fin = time.fromisoformat(reservation.hora_fin)
    except ValueError:
        raise HTTPException(status_code=400, detail="❌Formato de hora inválido. Use HH:MM:SS")
    
    # Validar duración de 1 hora
    duration = (hora_fin.hour * 60 + hora_fin.minute) - (hora_inicio.hour * 60 + hora_inicio.minute)
    if duration != 60:
        raise HTTPException(status_code=400, detail="❌La reserva debe ser exactamente de 1 hora")
    
    # Buscar o crear horario
    horario = db.exec(select(Horario).where(Horario.hora_inicio == hora_inicio, Horario.hora_fin == hora_fin)).first()
    if not horario:
        horario = Horario(hora_inicio=hora_inicio, hora_fin=hora_fin)
        db.add(horario)
        db.commit()
        db.refresh(horario)
    
    # Verificar solapamientos
    salas_res = db.exec(select(SalasReservacion).where(SalasReservacion.salas_id == reservation.sala_id)).all()
    reservaciones_ids = [sr.reservaciones_id for sr in salas_res]
    if reservaciones_ids:
        statement = select(Reservation).where(
            Reservation.id_reservaciones.in_(reservaciones_ids), # type:ignore
            Reservation.fecha == reservation.fecha,
            Reservation.estado != EstadoEnum.Cancelada
        )
        existing_reservations = db.exec(statement).all()
        for res in existing_reservations:
            h = db.exec(select(Horario).where(Horario.id_horario == res.horario_id)).first()
            if h and (hora_inicio < h.hora_fin and hora_fin > h.hora_inicio):
                raise HTTPException(status_code=400, detail="❌Conflicto de horario con otra reserva")
    
    if horario.id_horario is None:
        raise HTTPException(status_code=500, detail="❌No se pudo obtener el ID del horario")
    new_reservation = Reservation(
        fecha=reservation.fecha,
        estado=EstadoEnum.Confirmada,
        horario_id=horario.id_horario,
        sede_id=reservation.sede_id
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    # Relacionar usuario y sala con la reservación
    if new_reservation.id_reservaciones is None:
        raise HTTPException(status_code=500, detail="❌No se pudo obtener el ID de la nueva reservación")
    user_res = UsuarioReservacion(reservaciones_id=new_reservation.id_reservaciones, user_id=user_id)
    db.add(user_res)
    sala_res = SalasReservacion(reservaciones_id=new_reservation.id_reservaciones, salas_id=reservation.sala_id)
    db.add(sala_res)
    db.commit()
    return new_reservation

def get_reservations_me(db: Session, user_email: str):
    user_id = get_user_id_from_email(db, user_email)
    user_res = db.exec(select(UsuarioReservacion).where(UsuarioReservacion.user_id == user_id)).all()
    reservaciones_ids = [ur.reservaciones_id for ur in user_res]
    if reservaciones_ids:
        statement = select(Reservation).options(joinedload(Reservation.salas_reservaciones)).where(Reservation.id_reservaciones.in_(reservaciones_ids))  # type:ignore
        result = db.exec(statement)
        reservations = result.unique().all()
        response = []
        for res in reservations:
            sala_id = res.salas_reservaciones[0].salas_id if res.salas_reservaciones else None
            response.append({
                'id_reservaciones': res.id_reservaciones,
                'fecha': res.fecha,
                'estado': res.estado,
                'horario_id': res.horario_id,
                'sede_id': res.sede_id,
                'sala_id': sala_id
            })
        return response
    return []

def get_reservations_room(db: Session, room_id: int):
    salas_res = db.exec(select(SalasReservacion).where(SalasReservacion.salas_id == room_id)).all()
    reservaciones_ids = [sr.reservaciones_id for sr in salas_res]
    if reservaciones_ids:
        result = db.exec(select(Reservation).where(Reservation.id_reservaciones.in_(reservaciones_ids)))# type:ignore
        return result.all()
    return []

def get_reservations_date(db: Session, date_str: str):
    try:
        fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="❌Formato de fecha inválido. Use YYYY-MM-DD")
    result = db.exec(select(Reservation).where(Reservation.fecha == fecha))
    return result.all()

def cancel_reservation(db: Session, reservation_id: int, user_email: str):
    user = db.exec(select(Usuarios).where(Usuarios.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="❌Usuario no encontrado")
    user_id = user.id_user
    if user.rol == "Admin":
        # Admin can cancel any reservation
        pass
    else:
        user_res = db.exec(select(UsuarioReservacion).where(
            UsuarioReservacion.reservaciones_id == reservation_id,
            UsuarioReservacion.user_id == user_id
        )).first()
        if not user_res:
            raise HTTPException(status_code=403, detail="❌No tienes permiso para cancelar esta reserva")
    reservation = db.exec(select(Reservation).where(Reservation.id_reservaciones == reservation_id)).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="❌Reserva no encontrada")
    reservation.estado = EstadoEnum.Cancelada
    db.commit()
    db.refresh(reservation)
    return reservation
