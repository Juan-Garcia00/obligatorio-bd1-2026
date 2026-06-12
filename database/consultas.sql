
-- 1. Actividades con mayor cantidad de inscriptos confirmados
SELECT a.id, a.nombre, COUNT(*) AS total_confirmados
FROM inscripcion i
JOIN actividad a ON a.id = i.actividad_id
WHERE i.estado = 'CONFIRMADA'
GROUP BY a.id, a.nombre
ORDER BY total_confirmados DESC;


-- 2. Actividades con cupos disponibles
SELECT id AS id_actividad, nombre, cupo_maximo,
       (cupo_maximo - (SELECT COUNT(*) FROM inscripcion WHERE actividad_id = actividad.id AND estado = 'CONFIRMADA')) AS cupos_libres
FROM actividad
WHERE estado = 'ABIERTA'
  AND (cupo_maximo - (SELECT COUNT(*) FROM inscripcion WHERE actividad_id = actividad.id AND estado = 'CONFIRMADA')) > 0;


-- 3. Cantidad de inscriptos por disciplina deportiva
SELECT d.nombre AS disciplina, COUNT(i.id) AS total_inscriptos
FROM disciplina d
JOIN actividad a ON d.id = a.disciplina_id
JOIN inscripcion i ON a.id = i.actividad_id
GROUP BY d.id, d.nombre;


-- 4. Cantidad de inscriptos por carrera o facultad
SELECT c.nombre AS carrera, f.nombre AS facultad, COUNT(i.id) AS total_inscriptos
FROM estudiante e
JOIN carrera c ON e.carrera_id = c.id
JOIN facultad f ON e.facultad_id = f.id
JOIN inscripcion i ON e.id = i.estudiante_id
GROUP BY e.carrera_id, e.facultad_id, c.nombre, f.nombre;


-- 5. Porcentaje de ocupación de cada actividad
SELECT a.id AS id_actividad, a.nombre,
       ROUND((COUNT(i.id) / a.cupo_maximo) * 100, 2) AS porcentaje_ocupacion
FROM actividad a
LEFT JOIN inscripcion i ON a.id = i.actividad_id AND i.estado = 'CONFIRMADA'
GROUP BY a.id, a.nombre, a.cupo_maximo;


-- 6. Porcentaje de asistencia por actividad
SELECT a.id, a.nombre,
       ROUND((COUNT(CASE WHEN ast.presente = TRUE THEN 1 END) / COUNT(*)) * 100, 2) AS porcentaje_asistencia
FROM asistencia ast
JOIN actividad a ON a.id = ast.actividad_id
GROUP BY a.id, a.nombre


-- 7. Estudiantes con tres o más inasistencias registradas

SELECT e.documento, e.nombre, e.apellido, COUNT(*) AS total_inasistencias
FROM estudiante e
JOIN asistencia a ON e.id = a.estudiante_id
WHERE a.presente = FALSE
GROUP BY e.id, e.documento, e.nombre, e.apellido
HAVING total_inasistencias >= 3;

-- 8. Adicional 1: Estudiantes que están actualmente en Lista de Espera
SELECT e.nombre, e.apellido, a.nombre AS actividad, i.fecha_inscripcion
FROM estudiante e
JOIN inscripcion i ON e.id = i.estudiante_id
JOIN actividad a ON a.id = i.actividad_id
WHERE i.estado = 'ESPERA';


-- 9. Adicional 2: Espacios más utilizados (cantidad de actividades que se dan ahí)
SELECT
    esp.nombre AS espacio,
    COUNT(a.id) AS cantidad_de_actividades
FROM espacio esp
JOIN actividad a
ON esp.id = a.espacio_id
GROUP BY esp.id, esp.nombre
ORDER BY cantidad_de_actividades DESC;


-- 10. Adicional 3: Total de inscripciones por estado 
SELECT estado, COUNT(*) AS total
FROM inscripcion
GROUP BY estado;