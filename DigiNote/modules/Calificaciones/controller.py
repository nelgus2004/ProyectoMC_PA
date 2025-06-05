from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import CalificacionesQuimestre, CalificacionFinal, MatriculaAsignacion, Matricula, Estudiante, AsignacionCurso, PeriodoLectivo, Curso, Materia, Profesor


class CalificacionesController:
    def __init__(self):
        pass

    def show_calificaciones(self):
        try:
            finales = db.session.query(CalificacionFinal).all()
            resultados = []

            for final in finales:
                quimestres = final.quimestres

                # Aseguramos orden por nombre del quimestre (Q1, Q2)
                q1 = next((q for q in quimestres if q.Quimestre.lower() == "quimestre 1"), None)
                q2 = next((q for q in quimestres if q.Quimestre.lower() == "quimestre 2"), None)

                asignacion = final.matricula_asignacion
                matricula = asignacion.matricula
                estudiante = matricula.estudiante
                curso = asignacion.asignacion_curso
                profesor = curso.profesor
                materia = curso.materia

                resultados.append({
                    'Estudiante': f"{estudiante.Nombre} {estudiante.Apellido}",
                    'Cedula': estudiante.Cedula,
                    'Materia': materia.Nombre,
                    'Profesor': f"{profesor.Nombre} {profesor.Apellido}",
                    'Nivel': curso.curso.Nivel if curso.curso else matricula.Nivel,
                    'Paralelo': curso.curso.Paralelo if curso.curso else matricula.Paralelo,
                    'PromedioFinal': float(final.PromedioFinal or 0),

                    # Quimestre 1
                    'Q1_Autonoma': float(q1.NotaAutonoma) if q1 else None,
                    'Q1_Practica': float(q1.NotaPractica) if q1 else None,
                    'Q1_Leccion': float(q1.NotaLeccion) if q1 else None,
                    'Q1_Examen': float(q1.NotaExamen) if q1 else None,
                    'Q1_Promedio': float(q1.PromedioQuimestre) if q1 else None,

                    # Quimestre 2
                    'Q2_Autonoma': float(q2.NotaAutonoma) if q2 else None,
                    'Q2_Practica': float(q2.NotaPractica) if q2 else None,
                    'Q2_Leccion': float(q2.NotaLeccion) if q2 else None,
                    'Q2_Examen': float(q2.NotaExamen) if q2 else None,
                    'Q2_Promedio': float(q2.PromedioQuimestre) if q2 else None,
                })

            return resultados

        except SQLAlchemyError as e:
            print(f' * Error al obtener calificaciones: {e}')
            return []


    def add_calificacion(self, request):
        if request.method == 'POST':
            try:
                idMatriculaAsignacion = int(request.form.get('idMatriculaAsignacion'))
                quimestre = request.form.get('Quimestre')
                autonoma = float(request.form.get('NotaAutonoma', 0))
                practica = float(request.form.get('NotaPractica', 0))
                leccion = float(request.form.get('NotaLeccion', 0))
                examen = float(request.form.get('NotaExamen', 0))

                promedio = round((autonoma + practica + leccion + examen) / 4, 2)

                asignacionCurso = db.session.query(MatriculaAsignacion).get(idMatriculaAsignacion).asignaciones_curso
                final = CalificacionFinal(
                    idMatriculaAsignacion=idMatriculaAsignacion,
                    idAsignacionCurso=asignacionCurso.idAsignacion
                )
                
                db.session.add(final)
                db.session.flush()

                nueva = CalificacionesQuimestre(
                    idCalificacionFinal=final.idCalificacionFinal,
                    Quimestre=quimestre,
                    NotaAutonoma=autonoma,
                    NotaPractica=practica,
                    NotaLeccion=leccion,
                    NotaExamen=examen,
                    PromedioQuimestre=promedio
                )
                db.session.add(nueva)

                # Actualizar promedios en calificación final
                if quimestre == '1':
                    final.PromQuimestre1 = promedio
                elif quimestre == '2':
                    final.PromQuimestre2 = promedio

                q1 = final.PromQuimestre1 or 0
                q2 = final.PromQuimestre2 or 0
                final.PromedioFinal = round((q1 + q2) / 2, 2)

                db.session.commit()
                return ('Calificación registrada correctamente', 'successful')

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al registrar calificación: {e}')
                return ('ERROR: No se pudo registrar la calificación.', 'danger')

    def get_calificacion_by_id(self, id_matricula_asignacion, quimestre):
        try:
            calif_final = CalificacionFinal.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()
            if not calif_final:
                return {}

            calif_quimestre = CalificacionesQuimestre.query.filter_by(
                idCalificacionFinal=calif_final.idCalificacionFinal,
                Quimestre=quimestre
            ).first()

            if not calif_quimestre:
                return {}

            return {
                'idQuimestre': calif_quimestre.idQuimestre,
                'Quimestre': calif_quimestre.Quimestre,
                'NotaAutonoma': float(calif_quimestre.NotaAutonoma),
                'NotaPractica': float(calif_quimestre.NotaPractica),
                'NotaLeccion': float(calif_quimestre.NotaLeccion),
                'NotaExamen': float(calif_quimestre.NotaExamen),
                'PromedioQuimestre': float(calif_quimestre.PromedioQuimestre)
            }

        except SQLAlchemyError as e:
            print(f' * Error al obtener calificación del quimestre: {e}')
            return {}


    def update_calificacion(self, id, request):
        if request.method == 'POST':
            try:
                calif = db.session.get(CalificacionesQuimestre, id)
                if not calif:
                    return ('No se encontró la calificación para editar.', 'info')

                calif.NotaAutonoma = float(request.form.get('NotaAutonoma', 0))
                calif.NotaPractica = float(request.form.get('NotaPractica', 0))
                calif.NotaLeccion = float(request.form.get('NotaLeccion', 0))
                calif.NotaExamen = float(request.form.get('NotaExamen', 0))

                promedio = round((calif.NotaAutonoma + calif.NotaPractica + calif.NotaLeccion + calif.NotaExamen) / 4, 2)
                calif.PromedioQuimestre = promedio

                # Actualizar en calificación final
                final = calif.calificacion_final
                if final:
                    if calif.Quimestre == '1':
                        final.PromQuimestre1 = promedio
                    elif calif.Quimestre == '2':
                        final.PromQuimestre2 = promedio
                    q1 = final.PromQuimestre1 or 0
                    q2 = final.PromQuimestre2 or 0
                    final.PromedioFinal = round((q1 + q2) / 2, 2)

                db.session.commit()
                return ('Calificación actualizada correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al editar calificación: {e}')
                return ('ERROR: No se pudo editar la calificación.', 'danger')

    def delete_calificacion(self, id):
        try:
            calif = db.session.get(CalificacionesQuimestre, id)
            if not calif:
                return ('No se encontró la calificación para eliminar.', 'info')

            final = calif.calificacion_final
            quimestre = calif.Quimestre

            db.session.delete(calif)

            # Recalcular calificación final
            if final:
                if quimestre == '1':
                    final.PromQuimestre1 = 0
                elif quimestre == '2':
                    final.PromQuimestre2 = 0
                final.PromedioFinal = round(((final.PromQuimestre1 or 0) + (final.PromQuimestre2 or 0)) / 2, 2)

            db.session.commit()
            return ('Calificación eliminada correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar calificación: {e}')
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
