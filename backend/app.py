from flask import Flask
from flask_cors import CORS
from routes.estudiantes import estudiantes_bp
from routes.actividades import actividades_bp
from routes.inscripciones import inscripciones_bp
from routes.asistencias import asistencias_bp
from routes.disciplinas import disciplinas_bp
from routes.espacios import espacios_bp
from routes.carreras import carreras_bp
from routes.facultad import facultad_bp
from routes.reportes import reportes_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(estudiantes_bp)
app.register_blueprint(actividades_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(asistencias_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(espacios_bp)
app.register_blueprint(carreras_bp)
app.register_blueprint(facultad_bp)
app.register_blueprint(reportes_bp)

@app.route('/')
def home():
    return {"mensaje": "Servidor de Deportes Universitario Activo"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)