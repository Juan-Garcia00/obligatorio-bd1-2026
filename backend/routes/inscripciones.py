from flask import Blueprint, request, jsonify
from db import conectar

inscripciones_bp = Blueprint('inscripciones', __name__)

@inscripciones_bp.route('/inscribir', methods=['POST'])
def inscribir():
    data = request.json
    id_estudiante = data['id_estudiante']
    id_actividad = data['id_actividad']
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT estado, cupo FROM actividad WHERE id = {id_actividad}")
    actividad = cursor.fetchone()
    
    if not actividad or actividad[0] != 'abierta':
        return jsonify({"error": "La actividad no esta abierta"}), 400

    cursor.execute(f"SELECT * FROM inscripcion WHERE id_estudiante = {id_estudiante} AND id_actividad = {id_actividad}")
    if cursor.fetchone():
        return jsonify({"error": "El estudiante ya esta inscripto"}), 400

    cursor.execute(f"SELECT COUNT(*) FROM inscripcion WHERE id_actividad = {id_actividad} AND estado = 'confirmada'")
    cant_inscriptos = cursor.fetchone()[0]

    if cant_inscriptos < actividad[1]:
        estado_final = 'confirmada'
    else:
        estado_final = 'lista_de_espera'
    cursor.execute(f"INSERT INTO inscripcion (id_estudiante, id_actividad, fecha, estado) VALUES ({id_estudiante}, {id_actividad}, '2026-06-07', '{estado_final}')")
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Inscripcion registrada como {estado_final}"}), 200