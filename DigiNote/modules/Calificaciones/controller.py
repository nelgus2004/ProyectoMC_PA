from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import (
    CalificacionesQuimestre, CalificacionFinal,
    MatriculaAsignacion, Matricula,
    Estudiante, AsignacionCurso,
    Profesor, Materia
)

class CalificacionesController:
    def __init__(self):
        pass

    def show_calificaciones(self):
        try:
            registros = []
            asignaciones = db.session.query(MatriculaAsignacion)\
                .join(Matricula)\
                .join(Estudiante)\
                .join(AsignacionCurso)\
                .join(Profesor)\
                .join(Materia)\
                .all()
            
            for a in asignaciones:
                estudiante = a.matricula.estudiante
                curso = a.asignacion_curso
                profesor = curso.docente
                materia = curso.materia

                registros.append({
                    'idMatriculaAsignacion': a.idMatriculaAsignacion,
                    'Nombre': estudiante.nombre,
                    'Apellido': getattr(estudiante, 'apellido', ''),
                    'idAsignacion': curso.idAsignacion,
                    'Nivel': curso.nivel,
                    'Paralelo': curso.paralelo,
                    'NombreProfesor': profesor.nombre,
                    'ApellidoProfesor': getattr(profesor, 'apellido', ''),
                    'NombreMateria': materia.nombre,
                })
            return registros
        except Exception as e:
            print(f"* Error al obtener registros foráneos: {e}")
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

                # Obtener o crear calificación final para la asignación
                final = db.session.query(CalificacionFinal).filter_by(idMatriculaAsignacion=idMatriculaAsignacion).first()
                if not final:
                    final = CalificacionFinal(idMatriculaAsignacion=idMatriculaAsignacion)
                    db.session.add(final)
                    db.session.flush()  # Para obtener idCalificacionFinal

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

    def get_calificacion_by_id(self, id):
        try:
            calif = db.session.get(CalificacionesQuimestre, id)
            if not calif:
                return {}

            resultado = calif.to_dict()
            # Agregamos datos detallados de la asignación y estudiante para mostrar
            final = calif.calificacion_final
            asignacion = final.matricula_asignacion
            matricula = asignacion.matricula
            estudiante = matricula.estudiante
            curso = asignacion.asignacion_curso
            profesor = curso.docente
            materia = curso.materia

            resultado['estudiante_nombre'] = estudiante.nombre
            resultado['paralelo'] = curso.paralelo
            resultado['nivel'] = curso.nivel
            resultado['profesor_nombre'] = profesor.nombre
            resultado['materia_nombre'] = materia.nombre

            return resultado
        except SQLAlchemyError as e:
            print(f' * Error al obtener calificación: {e}')
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
