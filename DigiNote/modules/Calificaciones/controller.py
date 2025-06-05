from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import Calificacion, MatriculaAsignacion, Matricula, Estudiante, AsignacionCurso, Curso, Materia, Profesor, PeriodoLectivo

class CalificacionesController:
    def __init__(self):
        pass

    def show_calificaciones(self):
        try:
            calificaciones = db.session.query(Calificacion).all()
            resultados = []

            for c in calificaciones:
                asignacion = c.matricula_asignacion
                estudiante = asignacion.matricula.estudiante
                curso_asignado = c.asignaciones_curso
                curso = curso_asignado.curso
                profesor = curso_asignado.profesor
                materia = curso_asignado.materia

                resultados.append({
                    'Estudiante': f"{estudiante.Nombre} {estudiante.Apellido}",
                    'Cedula': estudiante.Cedula,
                    'Materia': materia.Nombre,
                    'Profesor': f"{profesor.Nombre} {profesor.Apellido}",
                    'Nivel': curso.Nivel,
                    'Paralelo': curso.Paralelo,
                    'NotaAutonoma1': float(c.NotaAutonoma1),
                    'NotaPractica1': float(c.NotaPractica1),
                    'NotaLeccion1': float(c.NotaLeccion1),
                    'NotaExamen1': float(c.NotaExamen1),
                    'PromQuimestre1': float(c.PromQuimestre1),
                    'NotaAutonoma2': float(c.NotaAutonoma2),
                    'NotaPractica2': float(c.NotaPractica2),
                    'NotaLeccion2': float(c.NotaLeccion2),
                    'NotaExamen2': float(c.NotaExamen2),
                    'PromQuimestre2': float(c.PromQuimestre2),
                    'PromedioFinal': float(c.PromedioFinal),
                })

            return resultados
        except SQLAlchemyError as e:
            print(f" * Error al mostrar calificaciones: {e}")
            return []

    def add_calificacion(self, request):
        if request.method == 'POST':
            try:
                idMatriculaAsignacion = int(request.form.get('idMatriculaAsignacion'))
                autonoma = float(request.form.get('NotaAutonoma', 0))
                practica = float(request.form.get('NotaPractica', 0))
                leccion = float(request.form.get('NotaLeccion', 0))
                examen = float(request.form.get('NotaExamen', 0))

                promedio = round((autonoma + practica + leccion + examen) / 4, 2)

                existente = Calificacion.query.filter_by(idMatriculaAsignacion=idMatriculaAsignacion).first()

                if not existente:
                    idAsignacionCurso = MatriculaAsignacion.query.get(idMatriculaAsignacion).asignaciones_curso.idAsignacion
                    existente = Calificacion(
                        idMatriculaAsignacion=idMatriculaAsignacion,
                        idAsignacionCurso=idAsignacionCurso
                    )
                    db.session.add(existente)

                existente.NotaAutonoma1 = autonoma
                existente.NotaPractica1 = practica
                existente.NotaLeccion1 = leccion
                existente.NotaExamen1 = examen
                existente.PromQuimestre1 = promedio

                existente.NotaAutonoma2 = autonoma
                existente.NotaPractica2 = practica
                existente.NotaLeccion2 = leccion
                existente.NotaExamen2 = examen
                existente.PromQuimestre2 = promedio

                q1 = existente.PromQuimestre1 or 0
                q2 = existente.PromQuimestre2 or 0
                existente.PromedioFinal = round((q1 + q2) / 2, 2)

                db.session.commit()
                return ('Calificación registrada correctamente', 'success')

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al registrar calificación: {e}")
                return ('ERROR: No se pudo registrar la calificación.', 'danger')

    def get_calificacion_by_id(self, id_matricula_asignacion):
        try:
            c = Calificacion.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()
            if not c:
                return {}

            return {
                'NotaAutonoma1': float(c.NotaAutonoma1),
                'NotaPractica1': float(c.NotaPractica1),
                'NotaLeccion1': float(c.NotaLeccion1),
                'NotaExamen1': float(c.NotaExamen1),
                'PromQuimestre1': float(c.PromQuimestre1),
                'NotaAutonoma2': float(c.NotaAutonoma2),
                'NotaPractica2': float(c.NotaPractica2),
                'NotaLeccion2': float(c.NotaLeccion2),
                'NotaExamen2': float(c.NotaExamen2),
                'PromQuimestre2': float(c.PromQuimestre2),
                'PromedioFinal': float(c.PromedioFinal),
            }

        except SQLAlchemyError as e:
            print(f" * Error al obtener calificación: {e}")
            return {}

    def update_calificacion(self, id_matricula_asignacion, request):
        if request.method == 'POST':
            try:
                calif = Calificacion.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()

                if not calif:
                    return ('No se encontró la calificación para editar.', 'info')

                autonoma = float(request.form.get('NotaAutonoma', 0))
                practica = float(request.form.get('NotaPractica', 0))
                leccion = float(request.form.get('NotaLeccion', 0))
                examen = float(request.form.get('NotaExamen', 0))
                promedio = round((autonoma + practica + leccion + examen) / 4, 2)

                calif.NotaAutonoma1 = autonoma
                calif.NotaPractica1 = practica
                calif.NotaLeccion1 = leccion
                calif.NotaExamen1 = examen
                calif.PromQuimestre1 = promedio

                calif.NotaAutonoma2 = autonoma
                calif.NotaPractica2 = practica
                calif.NotaLeccion2 = leccion
                calif.NotaExamen2 = examen
                calif.PromQuimestre2 = promedio

                q1 = calif.PromQuimestre1 or 0
                q2 = calif.PromQuimestre2 or 0
                calif.PromedioFinal = round((q1 + q2) / 2, 2)

                db.session.commit()
                return ('Calificación actualizada correctamente', 'success')

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al actualizar calificación: {e}")
                return ('ERROR: No se pudo actualizar la calificación.', 'danger')

    def delete_calificacion(self, id_matricula_asignacion):
        try:
            calif = Calificacion.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()
            if not calif:
                return ('No se encontró la calificación para eliminar.', 'info')

            db.session.delete(calif)
            db.session.commit()
            return ('Calificación eliminada correctamente.', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar calificación: {e}")
            return ('ERROR: No se pudo eliminar la calificación.', 'danger')

    def foreign_records(self):
        try:
            estudiantes = db.session.query(
                Estudiante.idEstudiante,
                Estudiante.Cedula,
                Estudiante.Nombre,
                Estudiante.Apellido
            ).join(Estudiante.matriculas) \
            .join(Matricula.matricula_asignacion) \
            .join(MatriculaAsignacion.asignaciones_curso) \
            .join(AsignacionCurso.periodo) \
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .distinct() \
            .all()

            return {'estudiantes': [dict(idEstudiante=e.idEstudiante, nombreCompleto=e.Nombre + ' ' + e.Apellido, cedula = e.Cedula) for e in estudiantes]}
        except SQLAlchemyError as e:
            print(f" * Error en foreign_records (filtrando con matrícula activa): {e}")
            return {'estudiantes': [] }
        
    def get_asignaciones_por_estudiante(self, id_estudiante):
        try:
            asignaciones = db.session.query(
                MatriculaAsignacion.idMatriculaAsignacion,
                AsignacionCurso.idAsignacion,
                Materia.Nombre.label('nombre_materia'),
                Profesor.Nombre.label('nombre_profesor'),
                Profesor.Apellido.label('apellido_profesor'),
                Curso.Nivel,
                Curso.Paralelo
            ).join(MatriculaAsignacion.matricula) \
            .join(MatriculaAsignacion.asignaciones_curso) \
            .join(AsignacionCurso.profesor) \
            .join(AsignacionCurso.materia) \
            .join(AsignacionCurso.curso) \
            .filter(Matricula.idEstudiante == id_estudiante) \
            .filter(AsignacionCurso.periodo.has(PeriodoLectivo.Estado == 'Activo')) \
            .all()

            resultado = []
            for a in asignaciones:
                resultado.append({
                    'idMatriculaAsignacion': a.idMatriculaAsignacion,
                    'idAsignacionCurso': a.idAsignacion,
                    'materia': a.nombre_materia,
                    'profesor': f'{a.nombre_profesor} {a.apellido_profesor}',
                    'nivel': a.Nivel,
                    'paralelo': a.Paralelo
                })

            return resultado
        except SQLAlchemyError as e:
            print(f' * Error al obtener asignaciones del estudiante: {e}')
            return []