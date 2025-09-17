-- Esquema de la base de datos para el proyecto de reservaciones

CREATE DATABASE IF NOT EXISTS gestor_salas;
USE gestor_salas;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    rol ENUM('Admin', 'User') DEFAULT 'User',
    contraseña VARCHAR(255) NOT NULL
);

-- Tabla de sedes
CREATE TABLE sedes (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

-- Tabla de salas
CREATE TABLE salas (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    capacidad INT NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL
);

-- Tabla de relación sedes-salas
CREATE TABLE sedes_salas (
    sedes_id INT NOT NULL,
    salas_id INT NOT NULL,
    PRIMARY KEY (sedes_id, salas_id),
    FOREIGN KEY (sedes_id) REFERENCES sedes(id_sede),
    FOREIGN KEY (salas_id) REFERENCES salas(id_sala)
);

-- Tabla de horarios
CREATE TABLE horario (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla de reservaciones
CREATE TABLE reservaciones (
    id_reservaciones INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    estado ENUM('Pendiente', 'Confirmada', 'Cancelada') DEFAULT 'Pendiente',
    horario_id INT NOT NULL,
    sede_id INT NOT NULL,
    FOREIGN KEY (horario_id) REFERENCES horario(id_horario),
    FOREIGN KEY (sede_id) REFERENCES sedes(id_sede)
);

-- Tabla de relación usuarios-reservaciones
CREATE TABLE usuarios_reservaciones (
    reservaciones_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (reservaciones_id, user_id),
    FOREIGN KEY (reservaciones_id) REFERENCES reservaciones(id_reservaciones),
    FOREIGN KEY (user_id) REFERENCES usuarios(id_user)
);

-- Tabla de relación salas-reservaciones
CREATE TABLE salas_reservaciones (
    reservaciones_id INT NOT NULL,
    salas_id INT NOT NULL,
    PRIMARY KEY (reservaciones_id, salas_id),
    FOREIGN KEY (reservaciones_id) REFERENCES reservaciones(id_reservaciones),
    FOREIGN KEY (salas_id) REFERENCES salas(id_sala)
);

-- Inserts iniciales para horarios
INSERT INTO horario (hora_inicio, hora_fin, disponible) VALUES
('08:00:00', '09:00:00', TRUE),
('09:00:00', '10:00:00', TRUE),
('10:00:00', '11:00:00', TRUE),
('11:00:00', '12:00:00', TRUE),
('12:00:00', '13:00:00', TRUE),
('13:00:00', '14:00:00', TRUE),
('14:00:00', '15:00:00', TRUE),
('15:00:00', '16:00:00', TRUE),
('16:00:00', '17:00:00', TRUE),
('17:00:00', '18:00:00', TRUE),
('18:00:00', '19:00:00', TRUE),
('19:00:00', '20:00:00', TRUE);

-- Inserts iniciales para sedes
INSERT INTO sedes (nombre) VALUES
('Bogotá'),
('Medellín'),
('Cali'),
('Barranquilla');

-- Inserts iniciales para salas (tipos de room)
INSERT INTO salas (nombre, capacidad, descripcion, precio) VALUES
('Sala Pequeña', 10, 'Sala equipada con proyector, pizarra blanca, WiFi, aire acondicionado y capacidad para 10 personas. Ideal para reuniones ejecutivas o sesiones de brainstorming.', 50.00),
('Sala Mediana', 20, 'Sala con proyector HD, sistema de sonido, pizarra interactiva, WiFi de alta velocidad, aire acondicionado y capacidad para 20 personas. Perfecta para presentaciones o talleres.', 100.00),
('Sala Grande', 50, 'Auditorio equipado con proyector 4K, sistema de sonido surround, escenario, micrófonos inalámbricos, WiFi, aire acondicionado central y capacidad para 50 personas. Diseñado para conferencias y eventos corporativos.', 200.00);

-- Inserts iniciales para sedes_salas (todas las sedes tienen las salas 1, 2 y 3)
INSERT INTO sedes_salas (sedes_id, salas_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 2), (2, 3),
(3, 1), (3, 2), (3, 3),
(4, 1), (4, 2), (4, 3);
