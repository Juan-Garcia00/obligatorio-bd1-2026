from flask import Blueprint, request, jsonify
from db import conectar

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    conn = conectar()
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
    conn = conectar()
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
    datos = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO estudiante
        (documento, nombre, apellido, email, carrera, facultad)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        datos['documento'],
        datos['nombre'],
        datos['apellido'],
        datos['email'],
        datos['carrera'],
        datos['facultad']
    ))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({
        "id": nuevo_id,
        "mensaje": "Estudiante creado correctamente"
    }), 201


@estudiantes_bp.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    datos = request.get_json()
    conn = conectar()
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
    cursor.execute("""
        UPDATE estudiante
        SET documento = %s,
            nombre = %s,
            apellido = %s,
            email = %s,
            carrera = %s,
            facultad = %s
        WHERE id = %s
    """, (
        datos['documento'],
        datos['nombre'],
        datos['apellido'],
        datos['email'],
        datos['carrera'],
        datos['facultad'],
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Estudiante actualizado correctamente"
    }), 200


@estudiantes_bp.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    conn = conectar()
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
    cursor.execute(
        "DELETE FROM estudiante WHERE id = %s",
        (id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Estudiante eliminado correctamente"
    }), 200