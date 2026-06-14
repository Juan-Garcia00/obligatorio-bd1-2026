from flask import Blueprint, jsonify
from db import conectar
from autenticacion import verificar_rol

reportes_bp = Blueprint('reportes', __name__)


@reportes_bp.route('/reportes/mas-confirmados', methods=['GET'])
def mas_confirmados():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id, a.nombre, COUNT(*) AS total_confirmados
        FROM inscripcion i
        JOIN actividad a ON a.id = i.actividad_id
        WHERE i.estado = 'CONFIRMADA'
        GROUP BY a.id, a.nombre
        ORDER BY total_confirmados DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/cupos-disponibles', methods=['GET'])
def cupos_disponibles():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id AS id_actividad, nombre, cupo_maximo,
               (cupo_maximo - (SELECT COUNT(*) FROM inscripcion
                                WHERE actividad_id = actividad.id AND estado = 'CONFIRMADA')) AS cupos_libres
        FROM actividad
        WHERE estado = 'ABIERTA'
          AND (cupo_maximo - (SELECT COUNT(*) FROM inscripcion
                               WHERE actividad_id = actividad.id AND estado = 'CONFIRMADA')) > 0
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/inscriptos-disciplina', methods=['GET'])
def inscriptos_por_disciplina():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.nombre AS disciplina, COUNT(i.id) AS total_inscriptos
        FROM disciplina d
        JOIN actividad a ON d.id = a.disciplina_id
        JOIN inscripcion i ON a.id = i.actividad_id
        GROUP BY d.id, d.nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/inscriptos-carrera-facultad', methods=['GET'])
def inscriptos_por_carrera_facultad():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.nombre AS carrera, f.nombre AS facultad, COUNT(i.id) AS total_inscriptos
        FROM estudiante e
        JOIN carrera c ON e.carrera_id = c.id
        JOIN facultad f ON e.facultad_id = f.id
        JOIN inscripcion i ON e.id = i.estudiante_id
        GROUP BY e.carrera_id, e.facultad_id, c.nombre, f.nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/ocupacion', methods=['GET'])
def porcentaje_ocupacion():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id AS id_actividad, a.nombre,
               ROUND((COUNT(i.id) / a.cupo_maximo) * 100, 2) AS porcentaje_ocupacion
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id = i.actividad_id AND i.estado = 'CONFIRMADA'
        GROUP BY a.id, a.nombre, a.cupo_maximo
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/asistencia', methods=['GET'])
def porcentaje_asistencia():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id, a.nombre,
               ROUND((COUNT(CASE WHEN ast.presente = TRUE THEN 1 END) / COUNT(*)) * 100, 2) AS porcentaje_asistencia
        FROM asistencia ast
        JOIN actividad a ON a.id = ast.actividad_id
        GROUP BY a.id, a.nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/inasistencias', methods=['GET'])
def estudiantes_con_inasistencias():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.documento, e.nombre, e.apellido, COUNT(*) AS total_inasistencias
        FROM estudiante e
        JOIN asistencia a ON e.id = a.estudiante_id
        WHERE a.presente = FALSE
        GROUP BY e.id, e.documento, e.nombre, e.apellido
        HAVING total_inasistencias >= 3
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/lista-espera', methods=['GET'])
def lista_espera():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.nombre, e.apellido, a.nombre AS actividad, i.fecha_inscripcion
        FROM estudiante e
        JOIN inscripcion i ON e.id = i.estudiante_id
        JOIN actividad a ON a.id = i.actividad_id
        WHERE i.estado = 'ESPERA'
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/espacios-utilizados', methods=['GET'])
def espacios_mas_utilizados():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT esp.nombre AS espacio, COUNT(a.id) AS cantidad_de_actividades
        FROM espacio esp
        JOIN actividad a ON esp.id = a.espacio_id
        GROUP BY esp.id, esp.nombre
        ORDER BY cantidad_de_actividades DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@reportes_bp.route('/reportes/inscripciones-por-estado', methods=['GET'])
def inscripciones_por_estado():
    error = verificar_rol(['DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT estado, COUNT(*) AS total
        FROM inscripcion
        GROUP BY estado
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200