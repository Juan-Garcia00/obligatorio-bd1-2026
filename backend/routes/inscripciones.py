from flask import Blueprint, request, jsonify
from autenticacion import verificar_rol
from db import conectar

inscripciones_bp = Blueprint('inscripciones', __name__)


@inscripciones_bp.route('/inscripciones', methods=['GET'])
def listar_inscripciones():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.*, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido, a.nombre AS actividad_nombre
        FROM inscripcion i
        JOIN estudiante e ON e.id = i.estudiante_id
        JOIN actividad a ON a.id = i.actividad_id
        ORDER BY i.fecha_inscripcion DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@inscripciones_bp.route('/actividades/<int:actividad_id>/inscripciones', methods=['GET'])
def listar_inscripciones_actividad(actividad_id):
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.*, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido, e.documento
        FROM inscripcion i
        JOIN estudiante e ON e.id = i.estudiante_id
        WHERE i.actividad_id = %s
        ORDER BY i.fecha_inscripcion
    """, (actividad_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@inscripciones_bp.route('/inscripciones', methods=['POST'])
def crear_inscripcion():
    error = verificar_rol(['ESTUDIANTE'])
    if error:
        return error
    
    datos = request.get_json()
    estudiante_id = datos.get('estudiante_id')
    actividad_id = datos.get('actividad_id')
    if not estudiante_id or not actividad_id:
        return jsonify({"error": "Debe enviar estudiante_id y actividad_id"}), 400
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM estudiante WHERE id = %s", (estudiante_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Estudiante no encontrado"}), 404
    cursor.execute("SELECT * FROM actividad WHERE id = %s", (actividad_id,))
    actividad = cursor.fetchone()
    if not actividad:
        cursor.close()
        conn.close()
        return jsonify({"error": "Actividad no encontrada"}), 404
    if actividad['estado'] != 'ABIERTA':
        cursor.close()
        conn.close()
        return jsonify({"error": "La actividad no está abierta"}), 400
    cursor.execute("SELECT id FROM inscripcion WHERE estudiante_id = %s AND actividad_id = %s",
                   (estudiante_id, actividad_id))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "El estudiante ya está inscripto"}), 400
    cursor.execute("SELECT COUNT(*) AS total FROM inscripcion WHERE actividad_id = %s AND estado = 'CONFIRMADA'",
                   (actividad_id,))
    total = cursor.fetchone()['total']
    estado = 'CONFIRMADA' if total < actividad['cupo_maximo'] else 'ESPERA'
    cursor.execute("INSERT INTO inscripcion (estudiante_id, actividad_id, estado) VALUES (%s, %s, %s)",
                   (estudiante_id, actividad_id, estado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"estado": estado}), 201

@inscripciones_bp.route('/inscripciones/<int:id>', methods=['DELETE'])
def cancelar_inscripcion(id):
    error = verificar_rol(['ESTUDIANTE', 'ADMIN'])
    if error:
        return error

    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inscripcion WHERE id = %s", (id,))
    inscripcion = cursor.fetchone()
    if not inscripcion:
        cursor.close()
        conn.close()
        return jsonify({"error": "Inscripción no encontrada"}), 404

    cursor_del = conn.cursor()
    cursor_del.execute("DELETE FROM inscripcion WHERE id = %s", (id,))

    if inscripcion['estado'] == 'CONFIRMADA':
        cursor.execute("""
            SELECT id FROM inscripcion
            WHERE actividad_id = %s AND estado = 'ESPERA'
            ORDER BY fecha_inscripcion ASC
            LIMIT 1
        """, (inscripcion['actividad_id'],))
        siguiente = cursor.fetchone()
        if siguiente:
            cursor_del.execute("UPDATE inscripcion SET estado = 'CONFIRMADA' WHERE id = %s", (siguiente['id'],))

    conn.commit()
    cursor.close()
    cursor_del.close()
    conn.close()
    return jsonify({"mensaje": "Inscripción cancelada correctamente"}), 200