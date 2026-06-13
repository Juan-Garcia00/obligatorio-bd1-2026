
INSERT INTO facultad (nombre) VALUES
('Facultad de Ingeniería y Tecnologías'),
('Facultad de Ciencias Empresariales'),
('Facultad de Ciencias de la Salud'),
('Facultad de Derecho'),
('Facultad de Comunicación y Diseño'),
('Facultad de Psicología'),
('Facultad de Ciencias Humanas'),
('Facultad de Arquitectura'),
('Facultad de Ciencias Agrarias'),
('Facultad de Educación');

INSERT INTO carrera (nombre) VALUES
('Ingeniería en Informática'),
('Ingeniería Civil'),
('Contador Público'),
('Administración de Empresas'),
('Medicina'),
('Nutrición'),
('Abogacía'),
('Diseño Gráfico'),
('Comunicación Social'),
('Psicología'),
('Arquitectura'),
('Veterinaria');

INSERT INTO disciplina (nombre, descripcion) VALUES
('Fútbol', 'Deporte de equipo en cancha de césped'),
('Básquetbol', 'Deporte de equipo en cancha cubierta'),
('Atletismo', 'Disciplinas de pista y campo'),
('Vóleibol', 'Deporte de equipo en cancha cubierta'),
('Yoga', 'Actividad de bienestar y flexibilidad'),
('Funcional', 'Entrenamiento físico general'),
('Gimnasio', 'Musculación y entrenamiento con pesas'),
('Natación', 'Disciplina acuática'),
('Tenis', 'Deporte de raqueta individual o dobles'),
('Rugby', 'Deporte de equipo de contacto');

INSERT INTO espacio (nombre, ubicacion, capacidad) VALUES
('Cancha 1', 'Complejo Deportivo - Planta Baja', 30),
('Cancha 2', 'Complejo Deportivo - Planta Baja', 22),
('Pista Atlética', 'Complejo Deportivo - Exterior', 40),
('Sala Fitness', 'Edificio B - Piso 1', 25),
('Sala de Yoga', 'Edificio B - Piso 2', 20),
('Gimnasio Principal', 'Edificio B - Piso 1', 35),
('Piscina Climatizada', 'Complejo Deportivo - Anexo', 28),
('Cancha de Tenis', 'Complejo Deportivo - Exterior', 8),
('Polideportivo', 'Edificio C - Planta Baja', 50),
('Salón Multiuso', 'Edificio A - Piso 3', 18);


INSERT INTO actividad
(nombre, disciplina_id, espacio_id, cupo_maximo, dia_semana, hora_inicio, hora_fin, estado)
VALUES
('Fútbol recreativo mixto', 1, 1, 20, 'MARTES', '18:00', '19:30', 'ABIERTA'),
('Fútbol competitivo', 1, 2, 18, 'JUEVES', '19:00', '20:30', 'ABIERTA'),
('Básquetbol libre', 2, 9, 15, 'LUNES', '17:00', '18:30', 'ABIERTA'),
('Atletismo inicial', 3, 3, 25, 'JUEVES', '17:00', '18:00', 'ABIERTA'),
('Atletismo avanzado', 3, 3, 15, 'MARTES', '07:00', '08:30', 'CERRADA'),
('Vóleibol mixto', 4, 9, 16, 'MIERCOLES', '18:00', '19:30', 'ABIERTA'),
('Yoga matutino', 5, 5, 20, 'LUNES', '08:00', '09:00', 'ABIERTA'),
('Yoga vespertino', 5, 5, 20, 'VIERNES', '18:00', '19:00', 'FINALIZADA'),
('Funcional mañana', 6, 4, 15, 'LUNES', '08:00', '09:00', 'ABIERTA'),
('Funcional tarde', 6, 4, 15, 'MIERCOLES', '17:00', '18:00', 'ABIERTA'),
('Natación libre', 8, 7, 12, 'VIERNES', '07:00', '08:00', 'ABIERTA'),
('Tenis recreativo', 9, 8, 4, 'SABADO', '10:00', '12:00', 'CANCELADA');

INSERT INTO estudiante (documento, nombre, apellido, email, carrera_id, facultad_id) VALUES
('50123456', 'Ana', 'Pérez', 'ana.perez@uni.edu', 1, 1),
('48999888', 'Luis', 'Gómez', 'luis.gomez@uni.edu', 4, 2),
('51222333', 'Sofía', 'Rodríguez', 'sofia.rodriguez@uni.edu', 5, 3),
('49887766', 'Mateo', 'Fernández', 'mateo.fernandez@uni.edu', 2, 1),
('50345678', 'Valentina', 'López', 'valentina.lopez@uni.edu', 7, 4),
('51456789', 'Bruno', 'Martínez', 'bruno.martinez@uni.edu', 9, 5),
('50567890', 'Camila', 'Sosa', 'camila.sosa@uni.edu', 10, 6),
('49678901', 'Joaquín', 'Díaz', 'joaquin.diaz@uni.edu', 3, 2),
('51789012', 'Martina', 'Castro', 'martina.castro@uni.edu', 11, 8),
('50890123', 'Tomás', 'Acosta', 'tomas.acosta@uni.edu', 1, 1),
('49901234', 'Lucía', 'Suárez', 'lucia.suarez@uni.edu', 6, 3),
('51012345', 'Agustín', 'Romero', 'agustin.romero@uni.edu', 12, 9),
('50123457', 'Florencia', 'Núñez', 'florencia.nunez@uni.edu', 8, 5),
('49234568', 'Nicolás', 'Vidal', 'nicolas.vidal@uni.edu', 2, 1),
('51345679', 'Paula', 'Méndez', 'paula.mendez@uni.edu', 4, 2);

-- Actividad 1: cupo 20
INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(1, 1, 'CONFIRMADA'),
(2, 1, 'CONFIRMADA'),
(3, 1, 'CONFIRMADA'),
(4, 1, 'CONFIRMADA'),
(5, 1, 'CONFIRMADA');

-- Actividad 3: cupo 15 (llenamos para probar lista de espera)
INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(6, 3, 'CONFIRMADA'),
(7, 3, 'CONFIRMADA'),
(8, 3, 'CONFIRMADA'),
(9, 3, 'ESPERA');

INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(10, 4, 'CONFIRMADA'),
(11, 4, 'CONFIRMADA');

INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(12, 7, 'CONFIRMADA'),
(13, 7, 'CONFIRMADA');

INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(14, 9, 'CONFIRMADA'),
(15, 9, 'CONFIRMADA');

-- Actividad 1, fecha 2026-06-02 y 2026-06-09
INSERT INTO asistencia (actividad_id, estudiante_id, fecha, presente) VALUES
(1, 1, '2026-06-02', TRUE),
(1, 2, '2026-06-02', TRUE),
(1, 3, '2026-06-02', FALSE),
(1, 4, '2026-06-02', TRUE),
(1, 5, '2026-06-02', FALSE),
(1, 1, '2026-06-09', TRUE),
(1, 3, '2026-06-09', FALSE),
(1, 5, '2026-06-09', FALSE);

-- Actividad 3, fecha 2026-06-03
INSERT INTO asistencia (actividad_id, estudiante_id, fecha, presente) VALUES
(3, 6, '2026-06-03', TRUE),
(3, 7, '2026-06-03', FALSE),
(3, 8, '2026-06-03', TRUE);

-- Estudiante 3 con 3+ inasistencias (para probar la consulta 7)
INSERT INTO asistencia (actividad_id, estudiante_id, fecha, presente) VALUES
(1, 3, '2026-06-16', FALSE);


INSERT INTO asistencia (actividad_id, estudiante_id, fecha, presente) VALUES
(4, 10, '2026-06-04', TRUE),
(4, 11, '2026-06-04', TRUE);


INSERT INTO asistencia (actividad_id, estudiante_id, fecha, presente) VALUES
(7, 12, '2026-06-08', TRUE);