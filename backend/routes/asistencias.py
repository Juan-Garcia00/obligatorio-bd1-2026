from flask import Blueprint, request, jsonify
from db import conectar

asistencias_bp = Blueprint('asistencias', __name__)

@asistencias_bp.route('/asistencia', methods=['POST'])
def registrar_asistencia():
    data = request.json
    id_inscripcion = data['id_inscripcion']
    fecha = data['fecha']
    asistio = data['asistio'] 
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT estado FROM inscripcion WHERE id = {id_inscripcion}")
    inscripcion = cursor.fetchone()
    
    if not inscripcion or inscripcion[0] != 'confirmada':
        return jsonify({"error": "No se puede dar asistencia a alguien que no este confirmado"}), 400
        
    cursor.execute(f"INSERT INTO asistencia (id_inscripcion, fecha, asistio) VALUES ({id_inscripcion}, '{fecha}', '{asistio}')")
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Asistencia grabada"}), 200