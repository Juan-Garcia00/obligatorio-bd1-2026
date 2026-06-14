from flask import Blueprint, request, jsonify
import mysql.connector
from autenticacion import verificar_rol
from db import conectar

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM estudiante
        ORDER BY apellido, nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@estudiantes_bp.route('/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM estudiante WHERE id = %s",
        (id,)
    )
    estudiante = cursor.fetchone()
    cursor.close()
    conn.close()
    if not estudiante:
        return jsonify({
            "error": "Estudiante no encontrado"
        }), 404
    return jsonify(estudiante), 200


@estudiantes_bp.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    error = verificar_rol(['ADMIN'])
    if error:
        return error

    datos = request.get_json()
    campos = ['documento', 'nombre', 'apellido', 'email', 'carrera_id', 'facultad_id']
    if not datos or not all(datos.get(c) for c in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO estudiante
            (documento, nombre, apellido, email, carrera_id, facultad_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            datos['documento'],
            datos['nombre'],
            datos['apellido'],
            datos['email'],
            datos['carrera_id'],
            datos['facultad_id']
        ))
        conn.commit()
        nuevo_id = cursor.lastrowid
    except mysql.connector.IntegrityError as err:
        conn.rollback()
        cursor.close()
        conn.close()
        if 'documento' in str(err):
            return jsonify({"error": "El documento ya existe"}), 400
        if 'email' in str(err):
            return jsonify({"error": "El email ya existe"}), 400
        return jsonify({"error": "carrera o facultad no encontrada"}), 400
    cursor.close()
    conn.close()
    return jsonify({
        "id": nuevo_id,
        "mensaje": "Estudiante creado correctamente"
    }), 201


@estudiantes_bp.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error

    datos = request.get_json()
    campos = ['documento', 'nombre', 'apellido', 'email', 'carrera_id', 'facultad_id']
    if not datos or not all(datos.get(c) for c in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM estudiante WHERE id = %s",
        (id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Estudiante no encontrado"
        }), 404
    try:
        cursor.execute("""
            UPDATE estudiante
            SET documento = %s,
                nombre = %s,
                apellido = %s,
                email = %s,
                carrera_id = %s,
                facultad_id = %s
            WHERE id = %s
        """, (
            datos['documento'],
            datos['nombre'],
            datos['apellido'],
            datos['email'],
            datos['carrera_id'],
            datos['facultad_id'],
            id
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.IntegrityError as err:
        conn.rollback()
        cursor.close()
        conn.close()
        if 'documento' in str(err):
            return jsonify({"error": "El documento ya existe"}), 400
        if 'email' in str(err):
            return jsonify({"error": "El email ya existe"}), 400
        return jsonify({"error": "carrera o facultad no encontrada"}), 400
    return jsonify({
        "mensaje": "Estudiante actualizado correctamente"
    }), 200


@estudiantes_bp.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM estudiante WHERE id = %s",
        (id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Estudiante no encontrado"
        }), 404
    try:
        cursor.execute(
            "DELETE FROM estudiante WHERE id = %s",
            (id,)
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({
            "error": "No se puede eliminar el estudiante porque tiene inscripciones asociadas"
        }), 400
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Estudiante eliminado correctamente"
    }), 200