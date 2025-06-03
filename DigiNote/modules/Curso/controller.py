from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import AsignacionCurso, Curso, Profesor, Materia, PeriodoLectivo
from datetime import timedelta, time

class CursoController:
    def __init__(self):
        pass

    def show_curso(self):
        try:
            # Cursos asignados
            data = db.session.query(
                AsignacionCurso.idAsignacion,
                Curso.Nivel,
                Curso.Paralelo,
                AsignacionCurso.HoraEntrada,
                AsignacionCurso.HoraSalida,
                AsignacionCurso.Aula,
                db.func.concat(Profesor.Apellido, ' ', Profesor.Nombre).label('Profesor'),
                Materia.Nombre.label('Materia'),
                db.func.concat(
                    PeriodoLectivo.Nombre, ' ',
                    db.func.date_format(PeriodoLectivo.FechaInicio, '%M'), '-',
                    db.func.date_format(PeriodoLectivo.FechaFin, '%M')
                ).label('Periodo')
            ).join(Curso).join(Profesor).join(Materia).join(PeriodoLectivo)\
            .filter(PeriodoLectivo.Estado == 'Activo')\
            .all()

            cursos = db.session.query(Curso).all()
 
            return {
                'asignacion': data,
                'cursos': cursos
            }

        except SQLAlchemyError as e:
            print(f' * Error al obtener cursos: {e}')
            return {'asignaciones': [], 'cursos': []}

    def add_curso(self, request):
        if request.method == 'POST':
            try:
                curso = AsignacionCurso(
                    idCurso=request.form.get('idCurso'),
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
                return ('ERROR: No se pudo añadir el curso.', 'danger')

    def get_curso_by_id(self, id):
        curso = db.session.get(AsignacionCurso, id)
        if not curso:
            return {}

        resultado = curso.to_dict()
        
        # Convertir campos time a string
        for campo in ['HoraEntrada', 'HoraSalida']:
            valor = getattr(curso, campo)
            if isinstance(valor, time):
                resultado[campo] = valor.strftime('%H:%M')
            elif isinstance(valor, timedelta):
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

                idCurso=request.form.get('idCurso')
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
                return ('ERROR: No se pudo editar el curso.', 'danger')

    def delete_curso(self, id):
        try:
            curso = db.session.get(AsignacionCurso, id)
            if not curso:
                return ('No se encontró el curso para eliminar.', 'info')
            db.session.delete(curso)
            db.session.commit()
            return ('Curso eliminado correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar curso: {e}')
            return ('ERROR: No se pudo eliminar el curso.', 'danger')

    def add_paralelo(self, request):
            if request.method == 'POST':
                try:
                    nuevo = Curso(
                        Nivel=request.form['Nivel'].strip(),
                        Paralelo=request.form['Paralelo'].strip()
                    )
                    db.session.add(nuevo)
                    db.session.commit()
                    
                    mensaje = ('Paralelo añadido correctamente', 'successful')
                    datos = {'id': nuevo.idCurso, 'nombre': f"{nuevo.Nivel} {nuevo.Paralelo}"}

                    return mensaje, datos
                except SQLAlchemyError as e:
                    db.session.rollback()
                    print(f' * Error al añadir paralelo: {e}')
                    mensaje = ('ERROR: No se pudo añadir el paralelo.', 'danger')
                    datos = {}

                    return mensaje, datos

    def delete_paralelo(self, id):
        try:
            paralelo = db.session.get(Curso, id)
            if not paralelo:
                return ('No se encontró el paralelo para eliminar.', 'info')
            db.session.delete(paralelo)
            db.session.commit()
            return ('Paralelo eliminado correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar paralelo: {e}')
            return ('ERROR: No se pudo eliminar el paralelo.', 'danger')


    def foreign_records(self):
        try:
            profesores = db.session.query(Profesor.idProfesor, Profesor.Nombre, Profesor.Apellido).all()
            materias = db.session.query(Materia.idMateria, Materia.Nombre).all()
            periodos = db.session.query(
                PeriodoLectivo.idPeriodo,
                PeriodoLectivo.Nombre,
                db.func.concat(
                    db.func.date_format(PeriodoLectivo.FechaInicio, '%M'),
                    '-',
                    db.func.date_format(PeriodoLectivo.FechaFin, '%M')
                ).label('Duracion')
            ).filter(PeriodoLectivo.Estado == 'Activo').all()

            return {
                'profesores': [dict(idProfesor=p.idProfesor, Nombre=p.Nombre, Apellido=p.Apellido) for p in profesores],
                'materias': [dict(idMateria=m.idMateria, Nombre=m.Nombre) for m in materias],
                'periodos': [dict(idPeriodo=p.idPeriodo, Nombre=p.Nombre, Duracion=p.Duracion) for p in periodos]
            }
        except SQLAlchemyError as e:
            print(f' * Error al obtener registros relacionados: {e}')
            return {'profesores': [], 'materias': [], 'periodos': []}
