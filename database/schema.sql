DROP DATABASE IF EXISTS sistema_deportes;
CREATE DATABASE sistema_deportes;
USE sistema_deportes;


CREATE TABLE facultad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE carrera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE estudiante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    carrera_id INT NOT NULL,
    facultad_id INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_estudiante_carrera FOREIGN KEY (carrera_id) REFERENCES carrera(id),
    CONSTRAINT fk_estudiante_facultad FOREIGN KEY (facultad_id) REFERENCES facultad(id)
);

CREATE TABLE disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NULL
);

CREATE TABLE espacio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    ubicacion VARCHAR(150) NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad > 0)
);

CREATE TABLE actividad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    disciplina_id INT NOT NULL,
    espacio_id INT NOT NULL,
    cupo_maximo INT NOT NULL CHECK (cupo_maximo > 0),
    dia_semana ENUM('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('ABIERTA','CERRADA','FINALIZADA','CANCELADA') NOT NULL DEFAULT 'ABIERTA',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_actividad_disciplina FOREIGN KEY (disciplina_id) REFERENCES disciplina(id),
    CONSTRAINT fk_actividad_espacio FOREIGN KEY (espacio_id) REFERENCES espacio(id),
    CONSTRAINT chk_horario CHECK (hora_fin > hora_inicio)
);

CREATE TABLE inscripcion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    actividad_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('CONFIRMADA','ESPERA') NOT NULL,
    CONSTRAINT fk_inscripcion_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiante(id),
    CONSTRAINT fk_inscripcion_actividad FOREIGN KEY (actividad_id) REFERENCES actividad(id),
    CONSTRAINT uq_inscripcion_unica UNIQUE (estudiante_id, actividad_id)
);

CREATE INDEX idx_inscripcion_actividad_estado
    ON inscripcion (actividad_id, estado);

CREATE TABLE asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad_id INT NOT NULL,
    estudiante_id INT NOT NULL,
    fecha DATE NOT NULL,
    presente BOOLEAN NOT NULL,
    registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_asistencia_actividad FOREIGN KEY (actividad_id) REFERENCES actividad(id),
    CONSTRAINT fk_asistencia_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiante(id),
    CONSTRAINT uq_asistencia_unica UNIQUE (actividad_id, estudiante_id, fecha)
);

CREATE INDEX idx_asistencia_actividad_fecha
    ON asistencia (actividad_id, fecha);
