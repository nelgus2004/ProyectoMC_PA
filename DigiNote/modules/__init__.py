from .inicio.route import index_bp
from .Profesor.route import profesor_bp
from .Estudiante.route import estudiante_bp
from .Curso.route import curso_bp
from .Asignatura.route import materia_bp
from .Calificaciones.route import calificacion_bp
from .Matricula.route import matricula_bp

all_routes = [
    (index_bp, '/app'),
    (profesor_bp, '/app/profesor'),
    (estudiante_bp, '/app/estudiante'),
    (curso_bp, '/app/curso'),
    (materia_bp, '/app/asignatura'),
    (calificacion_bp, '/app/calificacion'),
    (matricula_bp, '/app/matricula')
]
