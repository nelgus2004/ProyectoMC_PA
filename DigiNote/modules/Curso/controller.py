from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import AsignacionCurso, Profesor, Materia, PeriodoLectivo
from datetime import timedelta

class CursoController:
    def __init__(self):
        pass

    def show_curso(self):
        try:
            data = db.session.query(
                AsignacionCurso.idAsignacion,
                AsignacionCurso.Paralelo,
                AsignacionCurso.HoraEntrada,
                AsignacionCurso.HoraSalida,
                AsignacionCurso.Aula,
                db.func.concat(Profesor.Apellido, ' ', Profesor.Nombre).label('Profesor'),
                Materia.Nombre.label('Materia'),
                Materia.Nivel,
                db.func.concat(PeriodoLectivo.Nombre, ' ', 
                               db.func.date_format(PeriodoLectivo.FechaInicio, '%M'), '-',
                               db.func.date_format(PeriodoLectivo.FechaFin, '%M')).label('Periodo')
            ).join(Profesor).join(Materia).join(PeriodoLectivo)\
             .filter(PeriodoLectivo.Estado == 'Activo')\
             .all()
            return [row._asdict() for row in data]
        except SQLAlchemyError as e:
            print(f' * Error al obtener cursos: {e}')
            return []

    def add_curso(self, request):
        if request.method == 'POST':
            try:
                curso = AsignacionCurso(
                    Paralelo=request.form['Paralelo'].strip(),
                    HoraEntrada=request.form['HoraEntrada'],
                    HoraSalida=request.form['HoraSalida'],
                    Aula=request.form.get('Aula'),
                    idPeriodo=request.form.get('idPeriodo'),
                    idProfesor=request.form.get('idProfesor'),
                    idMateria=request.form.get('idMateria')
                )
                db.session.add(curso)
                db.session.commit()
                return ('Curso añadido correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al añadir curso: {e}')
                return ('ERROR: No se pudo añadir el curso.', 'error')

    def get_curso_by_id(self, id):
        curso = db.session.get(AsignacionCurso, id)
        if not curso:
            return {}
        
        resultado = curso.__dict__.copy()
        for campo in ['HoraEntrada', 'HoraSalida']:
            valor = getattr(curso, campo)
            if isinstance(valor, timedelta):
                total_seconds = valor.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                resultado[campo] = f'{hours:02}:{minutes:02}'
        resultado.pop('_sa_instance_state', None)
        return resultado

    def update_curso(self, id, request):
        if request.method == 'POST':
            try:
                curso = db.session.get(AsignacionCurso, id)
                if not curso:
                    return ('No se encontró el curso para editar.', 'info')

                curso.Paralelo = request.form['Paralelo'].strip()
                curso.HoraEntrada = request.form['HoraEntrada']
                curso.HoraSalida = request.form['HoraSalida']
                curso.Aula = request.form.get('Aula')
                curso.idPeriodo = request.form.get('idPeriodo')
                curso.idProfesor = request.form.get('idProfesor')
                curso.idMateria = request.form.get('idMateria')

                db.session.commit()
                return ('Curso editado correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al editar curso: {e}')
                return ('ERROR: No se pudo editar el curso.', 'error')

    def delete_curso(self, id):
        try:
            curso = db.session.get(AsignacionCurso, id)
            if not curso:
                return ('No se encontró el curso para eliminar.', 'info')
            db.session.delete(curso)
            db.session.commit()
            return ('Curso eliminado correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar curso: {e}')
            return ('ERROR: No se pudo eliminar el curso.', 'error')

    def foreign_records(self):
        try:
            profesores = db.session.query(Profesor.idProfesor, Profesor.Nombre, Profesor.Apellido).all()
            materias = db.session.query(Materia.idMateria, Materia.Nombre, Materia.Nivel).all()
            periodos = db.session.query(
                PeriodoLectivo.idPeriodo,
                PeriodoLectivo.Nombre,
                db.func.concat(db.func.date_format(PeriodoLectivo.FechaInicio, '%M'), '-', db.func.date_format(PeriodoLectivo.FechaFin, '%M')).label('Duracion')
            ).filter(PeriodoLectivo.Estado == 'Activo').all()
            return {
                'profesores': [p._asdict() for p in profesores],
                'materias': [m._asdict() for m in materias],
                'periodos': [p._asdict() for p in periodos]
            }
        except SQLAlchemyError as e:
            print(f' * Error al obtener registros relacionados: {e}')
            return {'profesores': [], 'materias': [], 'periodos': []}

    def list_curso(self):
        try:
            data = db.session.query(
                AsignacionCurso.idAsignacion,
                db.func.concat(Profesor.Nombre, ' ', Profesor.Apellido).label('Profesor'),
                Materia.Nombre.label('Materia'),
                Materia.Nivel,
                AsignacionCurso.Paralelo,
                PeriodoLectivo.Nombre.label('Periodo')
            ).join(Profesor).join(Materia).join(PeriodoLectivo)\
             .filter(PeriodoLectivo.Estado == 'Activo')\
             .order_by(PeriodoLectivo.Nombre, AsignacionCurso.Paralelo, Materia.Nombre)\
             .all()
            return [row._asdict() for row in data]
        except SQLAlchemyError as e:
            print(f' * Error al listar cursos: {e}')
            return []
