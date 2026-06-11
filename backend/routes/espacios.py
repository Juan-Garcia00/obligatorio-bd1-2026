from flask import Blueprint, request, jsonify
from db import conectar

espacios_bp = Blueprint('espacios', __name__)


@espacios_bp.route('/espacios', methods=['GET'])
def listar_espacios():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM espacio
        ORDER BY nombre
    """)

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(resultado), 200


@espacios_bp.route('/espacios', methods=['POST'])
def crear_espacio():

    datos = request.get_json()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO espacio
        (nombre, ubicacion, capacidad)
        VALUES (%s, %s, %s)
    """, (
        datos['nombre'],
        datos['ubicacion'],
        datos['capacidad']
    ))

    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "id": nuevo_id,
        "mensaje": "Espacio creado correctamente"
    }), 201