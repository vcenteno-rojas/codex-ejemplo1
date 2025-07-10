from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de datos
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'edad': self.edad
        }

# Ruta para listar estudiantes
@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([e.to_dict() for e in estudiantes])

# Ruta para registrar un nuevo estudiante
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.get_json()
    estudiante = Estudiante(nombre=data['nombre'], edad=data['edad'])
    db.session.add(estudiante)
    db.session.commit()
    return jsonify(estudiante.to_dict()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
