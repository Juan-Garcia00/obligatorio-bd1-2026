from flask import Blueprint, request, jsonify
from backend.autenticacion import verificar_rol
from db import conectar

actividades_bp = Blueprint('actividades', __name__)


@actividades_bp.route('/actividades', methods=['GET'])
def listar_actividades():
    error = verificar_rol(['ALUMNO', 'DOCENTE', 'ADMIN'])
    if error:
        return error


    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, d.nombre AS disciplina_nombre, e.nombre AS espacio_nombre
        FROM actividad a
        JOIN disciplina d ON d.id = a.disciplina_id
        JOIN espacio e ON e.id = a.espacio_id
        ORDER BY a.id
    """)
    resultado = cursor.fetchall()
    for actividad in resultado:
        actividad["hora_inicio"] = str(actividad["hora_inicio"])
        actividad["hora_fin"] = str(actividad["hora_fin"])
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@actividades_bp.route('/actividades', methods=['POST'])
def crear_actividad():
    error = verificar_rol(['ADMIN'])
    if error:
        return error

    datos = request.get_json()
    campos = ['nombre', 'disciplina_id', 'espacio_id', 'cupo_maximo', 'dia_semana', 'hora_inicio', 'hora_fin']
    if not datos or not all(datos.get(c) for c in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actividad (nombre, disciplina_id, espacio_id, cupo_maximo, dia_semana, hora_inicio, hora_fin, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (datos['nombre'], datos['disciplina_id'], datos['espacio_id'], datos['cupo_maximo'],
          datos['dia_semana'], datos['hora_inicio'], datos['hora_fin'], datos.get('estado', 'ABIERTA')))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": nuevo_id}), 201


@actividades_bp.route('/actividades/<int:id>', methods=['PUT'])
def actualizar_actividad(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error

    datos = request.get_json()
    if not datos or not datos.get('nombre'):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM actividad WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Actividad no encontrada"}), 404
    cursor.execute("""
        UPDATE actividad
        SET nombre = %s, disciplina_id = %s, espacio_id = %s, cupo_maximo = %s,
            dia_semana = %s, hora_inicio = %s, hora_fin = %s, estado = %s
        WHERE id = %s
    """, (datos['nombre'], datos['disciplina_id'], datos['espacio_id'], datos['cupo_maximo'],
          datos['dia_semana'], datos['hora_inicio'], datos['hora_fin'], datos['estado'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Actualizada"}), 200


@actividades_bp.route('/actividades/<int:id>', methods=['DELETE'])
def eliminar_actividad(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error
    
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM actividad WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Actividad no encontrada"}), 404
    cursor.execute("DELETE FROM actividad WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Eliminada"}), 200