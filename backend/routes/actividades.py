from flask import Blueprint, request, jsonify
from db import conectar

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/actividades', methods=['GET'])
def listar_actividades():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            a.id, 
            a.nombre, 
            d.nombre AS disciplina, 
            e.nombre AS espacio, 
            a.cupo_maximo AS cupo, 
            a.dia_semana AS dia, 
            TIME_FORMAT(a.hora_inicio, '%H:%i') AS horario, 
            a.estado
        FROM actividad a
        JOIN disciplina d ON a.disciplina_id = d.id
        JOIN espacio e ON a.espacio_id = e.id
    """
    
    cursor.execute(query)
    lista = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(lista), 200