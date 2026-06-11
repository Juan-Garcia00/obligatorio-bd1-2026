USE deportes_uni;

INSERT INTO disciplina (nombre) VALUES
('Fútbol'),('Básquetbol'),('Atletismo'),('Vóleibol'),('Yoga'),('Funcional'),('Gimnasio');

INSERT INTO espacio (nombre, ubicacion, capacidad) VALUES
('Cancha 1', 'Complejo Deportivo', 30),
('Pista Atlética', 'Complejo Deportivo', 40),
('Sala Fitness', 'Edificio B', 25);

INSERT INTO actividad
(nombre, disciplina_id, espacio_id, cupo_maximo, dia_semana, hora_inicio, hora_fin, estado)
VALUES
('Fútbol recreativo mixto', 1, 1, 20, 'MARTES', '18:00', '19:30', 'ABIERTA'),
('Atletismo inicial',       3, 2, 25, 'JUEVES', '17:00', '18:00', 'ABIERTA'),
('Funcional mañana',        6, 3, 15, 'LUNES',  '08:00', '09:00', 'ABIERTA');

INSERT INTO estudiante (documento, nombre, apellido, email, carrera, facultad) VALUES
('50123456','Ana','Pérez','ana.perez@uni.edu','Ingeniería','FING'),
('48999888','Luis','Gómez','luis.gomez@uni.edu','Economía','FCEA'),
('51222333','Sofía','Rodríguez','sofia.rodriguez@uni.edu','Medicina','FMED');

INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES
(1,1,'CONFIRMADA'),
(2,1,'CONFIRMADA'),
(3,1,'ESPERA');