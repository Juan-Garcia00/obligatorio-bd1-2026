from flask import Blueprint, request, jsonify
from db import conectar

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades', methods=['GET'])
def listar_actividades():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            a.*,
            d.nombre AS disciplina_nombre,
            e.nombre AS espacio_nombre
        FROM actividad a
        JOIN disciplina d
            ON d.id = a.disciplina_id
        JOIN espacio e
            ON e.id = a.espacio_id
        ORDER BY a.id
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@actividades_bp.route('/actividades/<int:id>', methods=['GET'])
def obtener_actividad(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            a.*,
            d.nombre AS disciplina_nombre,
            e.nombre AS espacio_nombre
        FROM actividad a
        JOIN disciplina d
            ON d.id = a.disciplina_id
        JOIN espacio e
            ON e.id = a.espacio_id
        WHERE a.id = %s
    """, (id,))
    actividad = cursor.fetchone()
    cursor.close()
    conn.close()
    if not actividad:
        return jsonify({
            "error": "Actividad no encontrada"
        }), 404
    return jsonify(actividad), 200


@actividades_bp.route('/actividades', methods=['POST'])
def crear_actividad():
    datos = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actividad
        (
            nombre,
            disciplina_id,
            espacio_id,
            cupo_maximo,
            dia_semana,
            hora_inicio,
            hora_fin,
            estado
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        datos['nombre'],
        datos['disciplina_id'],
        datos['espacio_id'],
        datos['cupo_maximo'],
        datos['dia_semana'],
        datos['hora_inicio'],
        datos['hora_fin'],
        datos.get('estado', 'ABIERTA')
    ))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({
        "id": nuevo_id,
        "mensaje": "Actividad creada correctamente"
    }), 201


@actividades_bp.route('/actividades/<int:id>', methods=['PUT'])
def actualizar_actividad(id):
    datos = request.get_json()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM actividad WHERE id = %s",
        (id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Actividad no encontrada"
        }), 404
    cursor.execute("""
        UPDATE actividad
        SET
            nombre = %s,
            disciplina_id = %s,
            espacio_id = %s,
            cupo_maximo = %s,
            dia_semana = %s,
            hora_inicio = %s,
            hora_fin = %s,
            estado = %s
        WHERE id = %s
    """, (
        datos['nombre'],
        datos['disciplina_id'],
        datos['espacio_id'],
        datos['cupo_maximo'],
        datos['dia_semana'],
        datos['hora_inicio'],
        datos['hora_fin'],
        datos['estado'],
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Actividad actualizada correctamente"
    }), 200


@actividades_bp.route('/actividades/<int:id>', methods=['DELETE'])
def eliminar_actividad(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM actividad WHERE id = %s",
        (id,)
    )
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Actividad no encontrada"
        }), 404
    cursor.execute(
        "DELETE FROM actividad WHERE id = %s",
        (id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Actividad eliminada correctamente"
    }), 200