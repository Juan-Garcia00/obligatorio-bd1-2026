from flask import Blueprint, jsonify
from db import conectar

carreras_bp = Blueprint('carreras', __name__)


@carreras_bp.route('/carreras', methods=['GET'])
def listar_carreras():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM carrera
        ORDER BY nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200