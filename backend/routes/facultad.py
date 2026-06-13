from flask import Blueprint, jsonify
from backend.autenticacion import verificar_rol
from db import conectar

facultad_bp = Blueprint('facultad', __name__)

@facultad_bp.route('/facultades', methods=['GET'])
def listar_facultades():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM facultad
        ORDER BY nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200