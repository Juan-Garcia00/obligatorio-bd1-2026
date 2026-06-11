from flask import Blueprint, request, jsonify
from db import conectar

asistencias_bp = Blueprint('asistencias', __name__)

@asistencias_bp.route('/asistencias', methods=['GET'])
def listar_asistencias():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            ast.*,
            e.nombre AS estudiante_nombre,
            e.apellido AS estudiante_apellido,
            a.nombre AS actividad_nombre
        FROM asistencia ast
        JOIN estudiante e ON e.id = ast.estudiante_id
        JOIN actividad a ON a.id = ast.actividad_id
        ORDER BY ast.fecha DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@asistencias_bp.route('/actividades/<int:actividad_id>/asistencias', methods=['GET'])
def listar_asistencias_actividad(actividad_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            ast.*,
            e.nombre AS estudiante_nombre,
            e.apellido AS estudiante_apellido
        FROM asistencia ast
        JOIN estudiante e ON e.id = ast.estudiante_id
        WHERE ast.actividad_id = %s
        ORDER BY ast.fecha DESC, e.apellido
    """, (actividad_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@asistencias_bp.route('/asistencias', methods=['POST'])
def registrar_asistencia():
    datos = request.get_json()
    estudiante_id = datos.get('estudiante_id')
    actividad_id = datos.get('actividad_id')
    fecha = datos.get('fecha')
    presente = datos.get('presente')
    if not estudiante_id or not actividad_id or not fecha:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Verificar actividad
    cursor.execute("SELECT id FROM actividad WHERE id = %s", (actividad_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Actividad no encontrada"}), 404

    # Verificar inscripción confirmada
    cursor.execute("""
        SELECT id
        FROM inscripcion
        WHERE estudiante_id = %s
        AND actividad_id = %s
        AND estado = 'CONFIRMADA'
    """, (estudiante_id, actividad_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({
            "error": "El estudiante no tiene inscripción confirmada"
        }), 400
    
    # Registrar asistencia
    cursor.execute("""
        INSERT INTO asistencia
        (actividad_id, estudiante_id, fecha, presente)
        VALUES (%s, %s, %s, %s)
    """, (actividad_id, estudiante_id, fecha, bool(presente)))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({
        "id": nuevo_id,
        "mensaje": "Asistencia registrada correctamente"
    }), 201


@asistencias_bp.route('/asistencias/<int:id>', methods=['PUT'])
def actualizar_asistencia(id):
    datos = request.get_json()
    if datos.get('presente') is None:
        return jsonify({"error": "Debe indicar si estuvo presente"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM asistencia WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Asistencia no encontrada"}), 404
    cursor.execute("""
        UPDATE asistencia
        SET presente = %s
        WHERE id = %s
    """, (bool(datos['presente']), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Asistencia actualizada correctamente"
    }), 200


@asistencias_bp.route('/asistencias/<int:id>', methods=['DELETE'])
def eliminar_asistencia(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM asistencia WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()

        return jsonify({"error": "Registro no encontrado"}), 404
    cursor.execute("DELETE FROM asistencia WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "mensaje": "Asistencia eliminada correctamente"
    }), 200