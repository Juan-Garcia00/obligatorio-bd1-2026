from flask import Blueprint, request, jsonify
from db import conectar

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    
    query = f"""INSERT INTO estudiante (cedula, nombre, apellido, email, carrera, facultad) 
                VALUES ('{data['cedula']}', '{data['nombre']}', '{data['apellido']}', '{data['email']}', '{data['carrera']}', '{data['facultad']}')"""
    cursor.execute(query)
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Estudiante creado"}), 201