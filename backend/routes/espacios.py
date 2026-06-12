from flask import Blueprint, request, jsonify
from db import conectar

espacios_bp = Blueprint('espacios', __name__)


@espacios_bp.route('/espacios', methods=['GET'])
def listar_espacios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM espacio ORDER BY nombre")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@espacios_bp.route('/espacios', methods=['POST'])
def crear_espacio():
    datos = request.get_json()
    if not datos or not datos.get('nombre') or not datos.get('ubicacion') or not datos.get('capacidad'):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO espacio (nombre, ubicacion, capacidad) VALUES (%s, %s, %s)",
                   (datos['nombre'], datos['ubicacion'], datos['capacidad']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": nuevo_id}), 201


@espacios_bp.route('/espacios/<int:id>', methods=['PUT'])
def actualizar_espacio(id):
    datos = request.get_json()
    if not datos or not datos.get('nombre') or not datos.get('ubicacion') or not datos.get('capacidad'):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE espacio SET nombre = %s, ubicacion = %s, capacidad = %s WHERE id = %s",
                   (datos['nombre'], datos['ubicacion'], datos['capacidad'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Actualizado"}), 200


@espacios_bp.route('/espacios/<int:id>', methods=['DELETE'])
def eliminar_espacio(id):
    conn = conectar()
    cursor = conn.cursor()