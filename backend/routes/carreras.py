from flask import Blueprint, jsonify
from autenticacion import verificar_rol
from db import conectar

carreras_bp = Blueprint('carreras', __name__)


@carreras_bp.route('/carreras', methods=['GET'])
def listar_carreras():
    error = verificar_rol(['ESTUDIANTE', 'DOCENTE', 'ADMIN'])
    if error:
        return error
    conn = conectar()
    conn.set_charset_collation('utf8mb4')
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