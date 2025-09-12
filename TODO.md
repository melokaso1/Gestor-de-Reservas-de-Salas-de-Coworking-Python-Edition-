# TODO List for Coworking Reservation API Project

## 1. Modelos
- [ ] Crear modelo Room en app/models/room/room.py
- [ ] Actualizar modelo Reservation en app/models/reservation/reservation.py para incluir sala_id, hora_inicio, hora_fin, usuario_id

## 2. Controladores
- [ ] Crear controlador Room en app/controllers/rooms/room_controller.py
- [ ] Implementar controlador Reservation en app/controllers/reservaciones/reservation_controllers.py con validaciones

## 3. Rutas
- [ ] Crear rutas Room en app/routes/rooms/room.py
- [ ] Crear rutas Reservation en app/routes/reservations/reservation.py

## 4. Configuración Principal
- [ ] Actualizar app/main.py para incluir nuevos routers
- [ ] Verificar y actualizar requirements.txt con dependencias necesarias

## 5. Base de Datos
- [ ] Crear tablas en la base de datos usando create_db_and_tables()

## 6. Pruebas y Validaciones
- [ ] Probar endpoints de autenticación
- [ ] Probar endpoints de usuarios
- [ ] Probar endpoints de salas
- [ ] Probar endpoints de reservas con validaciones de horarios
- [ ] Agregar reportes opcionales (solo admin)

## 7. Características Extra
- [ ] Implementar lógica de penalización por cancelaciones (opcional)
