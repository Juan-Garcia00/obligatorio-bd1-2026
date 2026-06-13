from flask import Blueprint, request, jsonify
from backend.autenticacion import verificar_rol
from db import conectar

disciplinas_bp = Blueprint('disciplinas', __name__)


@disciplinas_bp.route('/disciplinas', methods=['GET'])
def listar_disciplinas():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM disciplina ORDER BY nombre")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@disciplinas_bp.route('/disciplinas', methods=['POST'])
def crear_disciplina():
    error = verificar_rol(['ADMIN'])
    if error:
        return error
    datos = request.get_json()
    if not datos or not datos.get('nombre'):
        return jsonify({"error": "El nombre es obligatorio"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO disciplina (nombre, descripcion) VALUES (%s, %s)",
                   (datos['nombre'], datos.get('descripcion')))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": nuevo_id}), 201


@disciplinas_bp.route('/disciplinas/<int:id>', methods=['PUT'])
def actualizar_disciplina(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error
    datos = request.get_json()
    if not datos or not datos.get('nombre'):
        return jsonify({"error": "El nombre es obligatorio"}), 400
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE disciplina SET nombre = %s, descripcion = %s WHERE id = %s",
                   (datos['nombre'], datos.get('descripcion'), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Actualizada"}), 200


@disciplinas_bp.route('/disciplinas/<int:id>', methods=['DELETE'])
def eliminar_disciplina(id):
    error = verificar_rol(['ADMIN'])
    if error:
        return error
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disciplina WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Eliminada"}), 200