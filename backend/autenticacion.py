from flask import request, jsonify

roles_validos = ['ADMIN', 'ESTUDIANTE', 'DOCENTE']

def verificar_rol(roles_permitidos):

    # Recibe una lista de roles permitidos.
    # Devuelve None si está todo OK.
    # Devuelve (respuesta_error, codigo) si hay un problema.

    rol = request.headers.get('X-Rol')

    if not rol:
        return jsonify({'error': 'Falta el rol en el encabezado'}), 400
    
    if rol not in roles_validos:
        return jsonify({'error': 'Rol no válido'}), 403

    if rol not in roles_permitidos:
        return jsonify({'error': 'No tienes permiso para esta acción'}), 403
    
    return None