from flask import Flask
from flask_cors import CORS
from routes.estudiantes import estudiantes_bp
from routes.actividades import actividades_bp
from routes.inscripciones import inscripciones_bp
from routes.asistencias import asistencias_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(estudiantes_bp)
app.register_blueprint(actividades_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(asistencias_bp)

@app.route('/')
def home():
    return {"mensaje": "Servidor de Deportes Universitario Activo"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)