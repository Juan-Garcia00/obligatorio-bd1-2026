from flask import Blueprint, jsonify
from db import conectar

facultad_bp = Blueprint('facultad', __name__)

@facultad_bp.route('/facultades', methods=['GET'])
def listar_facultades():
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