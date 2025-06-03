from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import Estudiante, Materia, Matricula, MatriculaAsignacion, Profesor, Curso, AsignacionCurso, PeriodoLectivo
from datetime import date

class MatriculaController:
    def __init__(self):
        pass

    def show_matricula(self):
        try:
            matriculas = db.session.query(
                Matricula.idMatricula,
                Estudiante.Apellido,
                Estudiante.Nombre,
                Matricula.FechaMatricula,
                Matricula.Nivel,
                Matricula.Paralelo,
                Matricula.PromedioAnual
            ).join(Matricula.estudiante).all()

            asignaciones = db.session.query(
                MatriculaAsignacion.idMatricula,
                Materia.Nombre.label('Materia'),
                Curso.Paralelo,
                Curso.Nivel,
                Profesor.Apellido,
                Profesor.Nombre
            ).join(MatriculaAsignacion.asignacion) \
            .join(AsignacionCurso.materia) \
            .join(AsignacionCurso.profesor) \
            .join(AsignacionCurso.curso) \
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
                    FechaMatricula=request.form.get('FechaMatricula', date.today()),
                    Nivel=request.form['Nivel'],
                    Paralelo=request.form['Paralelo'],
                    PromedioAnual=request.form.get('PromedioAnual', 0)
                )

                db.session.add(nueva)
                db.session.flush()

                for id_asig in request.form.getlist('idAsignacion'):
                    db.session.add(MatriculaAsignacion(idMatricula=nueva.idMatricula, idAsignacion=id_asig))

                db.session.commit()
                return ('Matrícula creada correctamente con sus asignaciones.', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error en add_matricula: {e}")
                return ('ERROR: No se pudo registrar la matrícula.', 'danger')

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
                    return ('ERROR: Matrícula no encontrada.', 'danger')

                matricula.idEstudiante = request.form['idEstudiante']
                matricula.FechaMatricula = request.form.get('FechaMatricula', matricula.FechaMatricula)  # Usa la existente si no se envía
                matricula.Nivel = request.form['Nivel']
                matricula.Paralelo=request.form['Paralelo'],
                matricula.PromedioAnual = request.form.get('PromedioAnual', matricula.PromedioAnual)
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
                return ('ERROR: No se pudo actualizar la matrícula.', 'danger')

    def delete_matricula(self, id):
        try:
            matricula = db.session.get(Matricula, id)
            if not matricula:
                return ('No se encontró la matrícula para eliminar', 'info')

            db.session.query(MatriculaAsignacion).filter_by(idMatricula=id).delete()
            db.session.delete(matricula)
            db.session.commit()
            return ('Matrícula eliminada correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar matrícula: {e}")
            return ('ERROR: No se pudo eliminar la matrícula.', 'danger')

    def foreign_records(self):
        try:
            estudiantes = db.session.query(
                Estudiante.idEstudiante,
                Estudiante.Nombre,
                Estudiante.Apellido
            ).all()

            asignaciones = db.session.query(
                AsignacionCurso.idAsignacion,
                Materia.Nombre.label("Materia"),
                Curso.Nivel,
                Curso.Paralelo
            ).join(AsignacionCurso.materia) \
            .join(AsignacionCurso.curso) \
            .join(AsignacionCurso.periodo) \
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .all()

            asignaciones_list = [
                {
                    "idAsignacion": asig.idAsignacion,
                    "Materia": asig.Materia,
                    "Nivel": asig.Nivel,
                    "Paralelo": asig.Paralelo
                } for asig in asignaciones
            ]

            return {
                'estudiantes': [{'idEstudiante': e.idEstudiante, 'Nombre': f'{e.Apellido} {e.Nombre}'} for e in estudiantes ],
                'asignaciones': asignaciones_list
            }
        except SQLAlchemyError as e:
            print(f" * Error en foreign_records: {e}")
            return {
                'estudiantes': [],
                'asignaciones': []
            }
