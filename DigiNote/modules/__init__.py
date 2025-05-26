from .inicio.route import index_bp
from .Periodo.route import periodo_bp
from .Materia.route import materia_bp
from .Curso.route import curso_bp
from .Profesor.route import profesor_bp
from .Estudiante.route import estudiante_bp
from .Matricula.route import matricula_bp
from .Calificaciones.route import calificacion_bp
from .Usuario.route import usuario_bp

all_routes = [
    (index_bp, '/app'),
    (periodo_bp, '/app/periodo'),
    (materia_bp, '/app/asignatura'),
    (curso_bp, '/app/curso'),
    (profesor_bp, '/app/profesor'),
    (estudiante_bp, '/app/estudiante'),
    (matricula_bp, '/app/matricula'),
    (calificacion_bp, '/app/calificacion'),
    (usuario_bp, '/app/usuario')
]
