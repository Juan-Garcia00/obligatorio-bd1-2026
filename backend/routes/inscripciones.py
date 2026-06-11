from flask import Blueprint, request, jsonify
from db import conectar

inscripciones_bp = Blueprint('inscripciones', __name__)

@inscripciones_bp.route('/inscripciones', methods=['GET'])
def listar_inscripciones():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            i.*,
            e.nombre AS estudiante_nombre,
            e.apellido AS estudiante_apellido,
            a.nombre AS actividad_nombre
        FROM inscripcion i
        JOIN estudiante e
            ON e.id = i.estudiante_id
        JOIN actividad a
            ON a.id = i.actividad_id
        ORDER BY i.fecha_inscripcion DESC
    """)

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200

@inscripciones_bp.route('/actividades/<int:actividad_id>/inscripciones', methods=['GET'])
def listar_inscripciones_actividad(actividad_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            i.*,
            e.nombre AS estudiante_nombre,
            e.apellido AS estudiante_apellido,
            e.documento
        FROM inscripcion i
        JOIN estudiante e
            ON e.id = i.estudiante_id
        WHERE i.actividad_id = %s
        ORDER BY i.fecha_inscripcion
    """, (actividad_id,))

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@inscripciones_bp.route('/inscripciones', methods=['POST'])
def crear_inscripcion():
    datos = request.get_json()
    estudiante_id = datos.get('estudiante_id')
    actividad_id = datos.get('actividad_id')

    if not estudiante_id or not actividad_id:
        return jsonify({
            "error": "Debe enviar estudiante_id y actividad_id"
        }), 400
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Verificar estudiante
    cursor.execute(
        "SELECT id FROM estudiante WHERE id = %s",
        (estudiante_id,)
    )

    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Estudiante no encontrado"
        }), 404
    # Verificar actividad
    cursor.execute(
        "SELECT * FROM actividad WHERE id = %s",
        (actividad_id,)
    )
    actividad = cursor.fetchone()

    if not actividad:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Actividad no encontrada"
        }), 404
    
    # Verificar estado
    if actividad['estado'] != 'ABIERTA':
        cursor.close()
        conn.close()
        return jsonify({
            "error": "La actividad no está abierta"
        }), 400
    
    # Verificar inscripción duplicada
    cursor.execute("""
        SELECT id
        FROM inscripcion
        WHERE estudiante_id = %s
        AND actividad_id = %s
    """, (estudiante_id, actividad_id))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "El estudiante ya está inscripto"
        }), 400
    
    # Contar inscripciones confirmadas
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM inscripcion
        WHERE actividad_id = %s
        AND estado = 'CONFIRMADA'
    """, (actividad_id,))
    total = cursor.fetchone()['total']

    # Definir estado
    if total < actividad['cupo_maximo']:
        estado = 'CONFIRMADA'
    else:
        estado = 'ESPERA'

    # Insertar inscripción
    cursor.execute("""
        INSERT INTO inscripcion
        (estudiante_id, actividad_id, estado)
        VALUES (%s, %s, %s)
    """, (estudiante_id, actividad_id, estado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Inscripción creada correctamente",
        "estado": estado
    }), 201

@inscripciones_bp.route('/inscripciones/<int:id>', methods=['DELETE'])
def eliminar_inscripcion(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id FROM inscripcion WHERE id = %s",
        (id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Inscripción no encontrada"
        }), 404
    cursor.execute(
        "DELETE FROM inscripcion WHERE id = %s",
        (id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Inscripción eliminada correctamente"
    }), 200