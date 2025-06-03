from flask import request
from DigiNote.database import db
from DigiNote.database.models import Estudiante, Matricula, MatriculaAsignacion, AsignacionCurso, Curso
from sqlalchemy.exc import SQLAlchemyError

class EstudianteController:
    def show_estudiante(self):
        return Estudiante.query.all()

    def add_estudiante(self, request):
        if request.method == 'POST':
            try:
                estudiante = Estudiante(
                    Cedula=request.form['Cedula'],
                    Nombre=request.form['Nombre'].strip().title(),
                    Apellido=request.form['Apellido'].strip().title(),
                    FechaNacimiento=request.form['FechaNacimiento'],
                    Correo=request.form['Correo'],
                    Telefono=request.form.get('Telefono'),
                    Direccion=request.form.get('Direccion', ''),
                    Observacion=request.form.get('Observacion')
                )
                db.session.add(estudiante)
                db.session.commit()
                return ('Estudiante añadido correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al añadir estudiante: {e}')
                return ('ERROR: No se pudo añadir al estudiante.', 'danger')

    def get_estudiante_by_id(self, id):
        return Estudiante.query.get(id)

    def update_estudiante(self, id, request):
        if request.method == 'POST':
            try:
                estudiante = Estudiante.query.get(id)
                if not estudiante:
                    return ('Estudiante no encontrado', 'danger')
                estudiante.Cedula = request.form['Cedula']
                estudiante.Nombre = request.form['Nombre'].strip().title()
                estudiante.Apellido = request.form['Apellido'].strip().title()
                estudiante.FechaNacimiento = request.form['FechaNacimiento']
                estudiante.Correo = request.form['Correo']
                estudiante.Telefono = request.form.get('Telefono')
                estudiante.Direccion = request.form.get('Direccion', '')
                estudiante.Observacion = request.form.get('Observacion')
                db.session.commit()
                return ('Estudiante editado correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al actualizar estudiante: {e}')
                return ('ERROR: No se pudo actualizar el estudiante.', 'danger')

    def delete_estudiante(self, id):
        try:
            estudiante = Estudiante.query.get(id)
            if not estudiante:
                return ('No se encontró el estudiante para eliminar', 'info')
            db.session.delete(estudiante)
            db.session.commit()
            return ('Estudiante eliminado correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar estudiante: {e}')
            return ('ERROR: No se pudo eliminar el estudiante.', 'danger')
        
    def all_data_estudiantes(self, nivel=None, paralelo=None, id_periodo=None):
        query = db.session.query(
            Estudiante,
            Matricula,
            Curso.Nivel.label('NivelCurso'),
            Curso.Paralelo,
            AsignacionCurso.idPeriodo,
        )\
        .outerjoin(Matricula, Estudiante.idEstudiante == Matricula.idEstudiante)\
        .outerjoin(MatriculaAsignacion, Matricula.idMatricula == MatriculaAsignacion.idMatricula)\
        .outerjoin(AsignacionCurso, MatriculaAsignacion.idAsignacion == AsignacionCurso.idAsignacion)\
        .outerjoin(Curso, AsignacionCurso.idCurso == Curso.idCurso)

        valid_niveles = {"1ro", "2do", "3ro"}
        if nivel in valid_niveles:
            query = query.filter(Curso.Nivel == nivel)

        if paralelo:
            query = query.filter(Curso.Paralelo == paralelo)

        if id_periodo:
            query = query.filter(AsignacionCurso.idPeriodo == id_periodo)

        resultados = []
        for est, mat, nivel_val, paralelo_val, periodo_val in query.all():
            resultados.append({
                'idEstudiante': est.idEstudiante,
                'Cedula': est.Cedula,
                'Nombre': est.Nombre,
                'Apellido': est.Apellido,
                'FechaNacimiento': est.FechaNacimiento.strftime("%Y-%m-%d") if est.FechaNacimiento else None,
                'Correo': est.Correo,
                'Telefono': est.Telefono,
                'Direccion': est.Direccion,
                'Observacion': est.Observacion,
                'NivelCurso': nivel_val,
                'Paralelo': paralelo_val,
                'idPeriodo': periodo_val
            })

        return resultados

