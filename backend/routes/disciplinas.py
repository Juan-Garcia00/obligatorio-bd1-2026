from flask import Blueprint, request, jsonify
from db import conectar

disciplinas_bp = Blueprint('disciplinas', __name__)


@disciplinas_bp.route('/disciplinas', methods=['GET'])
def listar_disciplinas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM disciplina
        ORDER BY nombre
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200


@disciplinas_bp.route('/disciplinas', methods=['POST'])
def crear_disciplina():

    datos = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO disciplina
        (nombre, descripcion)
        VALUES (%s, %s)
    """, (
        datos['nombre'],
        datos.get('descripcion')
    ))

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Disciplina creada correctamente"
    }), 201