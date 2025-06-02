from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import ( Estudiante, Materia, Matricula, MatriculaAsignacion, Profesor, AsignacionCurso, PeriodoLectivo )

from ..Estudiante.controller import EstudianteController
from ..Curso.controller import CursoController
from ..Calificaciones.controller import CalificacionesController


class MatriculaController:
    def __init__(self):
        self.estudiante = EstudianteController()
        self.curso = CursoController()
        self.calificacion = CalificacionesController()

    def show_matricula(self):
        try:
            matriculas = db.session.query(
                Matricula.idMatricula,
                Estudiante.Apellido,
                Estudiante.Nombre,
                Matricula.FechaMatricula,
                Matricula.Nivel,
                Matricula.PromedioAnual
            ).join(Matricula.estudiante).all()

            asignaciones = db.session.query(
                MatriculaAsignacion.idMatricula,
                Materia.Nombre.label('Materia'),
                AsignacionCurso.Paralelo,
                Profesor.Apellido,
                Profesor.Nombre
            ).join(MatriculaAsignacion.asignacion) \
            .join(AsignacionCurso.materia) \
            .join(AsignacionCurso.profesor) \
            .join(AsignacionCurso.periodo) \
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .all()

            return (matriculas, asignaciones)
        except SQLAlchemyError as e:
            print(f" * Error al obtener matrículas: {e}")
            return ([], [])

    def add_matricula(self, request):
        if request.method == 'POST':
            try:
                nueva = Matricula(
                    idEstudiante=request.form['idEstudiante'],
                    FechaMatricula=request.form['FechaMatricula'],
                    Nivel=request.form['Nivel'],
                    PromedioAnual=request.form.get('PromedioAnual', 0)
                )
                db.session.add(nueva)
                db.session.flush()  # Obtener ID antes del commit

                for id_asig in request.form.getlist('idAsignacion'):
                    db.session.add(MatriculaAsignacion(idMatricula=nueva.idMatricula, idAsignacion=id_asig))

                db.session.commit()
                return ('Matrícula creada correctamente con sus asignaciones.', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error en add_matricula: {e}")
                return ('ERROR: No se pudo registrar la matrícula.', 'error')

    def get_matricula_by_id(self, id):
        try:
            matricula = db.session.get(Matricula, id)
            if not matricula:
                return {}

            asignaciones = [ma.idAsignacion for ma in matricula.asignaciones]
            result = {
                'idMatricula': matricula.idMatricula,
                'idEstudiante': matricula.idEstudiante,
                'FechaMatricula': matricula.FechaMatricula.isoformat(),
                'Nivel': matricula.Nivel,
                'PromedioAnual': matricula.PromedioAnual,
                'asignaciones': asignaciones
            }
            return result
        except SQLAlchemyError as e:
            print(f" * Error en get_matricula_by_id: {e}")
            return {}

    def update_matricula(self, id, request):
        if request.method == 'POST':
            try:
                matricula = db.session.get(Matricula, id)
                if not matricula:
                    return ('ERROR: Matrícula no encontrada.', 'error')

                matricula.idEstudiante = request.form['idEstudiante']
                matricula.FechaMatricula = request.form['FechaMatricula']
                matricula.Nivel = request.form['Nivel']
                matricula.PromedioAnual = self.calificacion.promedioAnual()

                nuevas_asignaciones = set(request.form.getlist('idAsignacion'))
                actuales_asignaciones = {str(ma.idAsignacion) for ma in matricula.asignaciones}

                # Eliminar las que ya no están
                for ma in list(matricula.asignaciones):
                    if str(ma.idAsignacion) not in nuevas_asignaciones:
                        db.session.delete(ma)

                # Añadir las nuevas
                for id_asig in nuevas_asignaciones - actuales_asignaciones:
                    db.session.add(MatriculaAsignacion(idMatricula=id, idAsignacion=id_asig))

                db.session.commit()
                return ('Matrícula actualizada correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al actualizar matrícula: {e}")
                return ('ERROR: No se pudo actualizar la matrícula.', 'error')

    def delete_matricula(self, id):
        try:
            matricula = db.session.get(Matricula, id)
            if not matricula:
                return ('No se encontró la matrícula para eliminar', 'info')

            db.session.query(MatriculaAsignacion).filter_by(idMatricula=id).delete()
            db.session.delete(matricula)
            db.session.commit()
            return ('Matrícula eliminada correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar matrícula: {e}")
            return ('ERROR: No se pudo eliminar la matrícula.', 'error')

    def foreign_records(self):
        return {
            'estudiantes': self.estudiante.list_estudiantes(),
            'asignaciones': self.curso.list_curso()
        }
