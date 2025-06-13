from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from DigiNote.database import db
from DigiNote.database.models import Calificacion, MatriculaAsignacion, Matricula, Estudiante, AsignacionCurso, Curso, Materia, Profesor, PeriodoLectivo

class CalificacionesController:
    def __init__(self):
        pass

    def show_calificaciones(self):
        try:
            estudiantes = db.session.query(
                Estudiante.idEstudiante,
                Estudiante.Cedula,
                Estudiante.Nombre,
                Estudiante.Apellido,
                Matricula.Nivel,
                Matricula.Paralelo,
                Matricula.PromedioAnual
            ).join(Matricula, Matricula.idEstudiante == Estudiante.idEstudiante)\
            .join(MatriculaAsignacion, MatriculaAsignacion.idMatricula == Matricula.idMatricula)\
            .join(PeriodoLectivo, PeriodoLectivo.idPeriodo == Matricula.idPeriodo)\
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .group_by(Estudiante.idEstudiante)\
            .all()
            
            resultado = [{
                'idEstudiante': est.idEstudiante,
                'nombreCompleto': f'{est.Nombre} {est.Apellido}',
                'cedula': est.Cedula,
                'nivel': est.Nivel,
                'paralelo': est.Paralelo,
                'promedio': float(est.PromedioAnual) if est.PromedioAnual else 0
            } for est in estudiantes]

            return resultado
        except SQLAlchemyError as e:
            print(f' * Error al mostrar calificaciones: {e}')
            return []            
             

    def add_calificacion(self, request):
        if request.method == 'POST':
            try:
                idMatriculaAsignacion = int(request.form.get('idMatriculaAsignacion'))

                existente = Calificacion.query.filter_by(idMatriculaAsignacion=idMatriculaAsignacion).first()

                if not existente:
                    idCursoAsignacion = MatriculaAsignacion.query.get(idMatriculaAsignacion).asignaciones_curso.idCursoAsignacion
                    existente = Calificacion(
                        idMatriculaAsignacion=idMatriculaAsignacion,
                        idAsignacionCurso=idCursoAsignacion
                    )
                    db.session.add(existente)


                existente.NotaAutonoma1 = float(request.form.get('NotaAutonoma1', 0))
                existente.NotaPractica1 = float(request.form.get('NotaPractica1', 0))
                existente.NotaLeccion1 = float(request.form.get('NotaLeccion1', 0))
                existente.NotaExamen1 = float(request.form.get('NotaExamen1', 0))
                existente.PromQuimestre1 = round((existente.NotaAutonoma1 + existente.NotaPractica1 + existente.NotaLeccion1 + existente.NotaExamen1) / 4, 2)

                existente.NotaAutonoma2 = float(request.form.get('NotaAutonoma2', 0))
                existente.NotaPractica2 = float(request.form.get('NotaPractica2', 0))
                existente.NotaLeccion2 = float(request.form.get('NotaLeccion2', 0))
                existente.NotaExamen2 = float(request.form.get('NotaExamen2', 0))
                existente.PromQuimestre2 = round((existente.NotaAutonoma2 + existente.NotaPractica2 + existente.NotaLeccion2 + existente.NotaExamen2) / 4, 2)

                q1 = existente.PromQuimestre1 or 0
                q2 = existente.PromQuimestre2 or 0

                db.session.commit()
                
                id_matricula = db.session.query(MatriculaAsignacion.idMatricula).filter_by(idMatriculaAsignacion=idMatriculaAsignacion).scalar()
                self.actualizar_promedio_anual(id_matricula=id_matricula)

                
                return { 'mensaje': ('Calificación registrada correctamente', 'success') }

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al registrar calificación: {e}')
                return { 'mensaje': ('No se pudo registrar la calificación.', 'danger') }


    def get_calificacion_by_id(self, id_estudiante):
        try:
            matricula = db.session.query(Matricula)\
                .filter(Matricula.idEstudiante == id_estudiante)\
                .order_by(Matricula.FechaMatricula.desc())\
                .first()
            
            if not matricula:
                return {'mensaje': (f'El estudiante no tiene matrículas registradas', 'danger')}
            
            calificaciones = db.session.query(
                Materia.Nombre.label('materia'),
                Profesor.Nombre.label('profesor_nombre'),
                Profesor.Apellido.label('profesor_apellido'),
                Calificacion
            )\
            .select_from(Calificacion)\
            .join(MatriculaAsignacion, Calificacion.idMatriculaAsignacion == MatriculaAsignacion.idMatriculaAsignacion)\
            .join(AsignacionCurso, MatriculaAsignacion.idCursoAsignacion == AsignacionCurso.idCursoAsignacion)\
            .join(Materia, AsignacionCurso.idMateria == Materia.idMateria)\
            .join(Profesor, AsignacionCurso.idProfesor == Profesor.idProfesor)\
            .filter(MatriculaAsignacion.idMatricula == matricula.idMatricula)\
            .all()
            
            resultado = {
                'idEstudiante': matricula.idEstudiante,
                'estudiante': f'{matricula.estudiante.Apellido} {matricula.estudiante.Nombre}',
                'cedula': matricula.estudiante.Cedula,
                'nivel': matricula.Nivel,
                'paralelo': matricula.Paralelo,
                'materias': []
            }
              
            for materia, profesor_nombre, profesor_apellido, calificacion in calificaciones:
                resultado['materias'].append({
                    'idCalificacion': calificacion.idCalificacion,
                    'idMatriculaAsignacion': calificacion.idMatriculaAsignacion,
                    'materia': materia,
                    'profesor': f'{profesor_nombre} {profesor_apellido}',
                    'notas': {
                        'primer_quimestre': {
                            'autonoma': float(calificacion.NotaAutonoma1),
                            'practica': float(calificacion.NotaPractica1),
                            'leccion': float(calificacion.NotaLeccion1),
                            'examen': float(calificacion.NotaExamen1),
                            'promedio': float(calificacion.PromQuimestre1)
                        },
                        'segundo_quimestre': {
                            'autonoma': float(calificacion.NotaAutonoma2),
                            'practica': float(calificacion.NotaPractica2),
                            'leccion': float(calificacion.NotaLeccion2),
                            'examen': float(calificacion.NotaExamen2),
                            'promedio': float(calificacion.PromQuimestre2)
                        },
                        'final': float(calificacion.PromedioFinal)
                    }
                })
            
            mensaje = (f'Calificaciones de {resultado.get("estudiante", "estudiante")} encontrados', 'info')
            
            if not resultado['materias']:
                mensaje = (f'El estudiante {resultado.get("estudiante", "estudiante")} no tiene matrículas asignadas', 'danger')
            
            return { 'mensaje': mensaje,
                     'resultado': resultado }

        except SQLAlchemyError as e:
            print(f'Error al obtener calificaciones: {e}')
            return { 'mensaje': ('Ocurrió un error al obtener las calificaciones', 'error') }


    def update_calificacion(self, id_matricula_asignacion, request):
        if request.method == 'POST':
            try:
                calif = Calificacion.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()

                if not calif:
                    return { 'mensaje': ('No se encontró la calificación para editar.', 'info') }

                autonoma1 = float(request.form.get('NotaAutonoma1', 0))
                practica1 = float(request.form.get('NotaPractica1', 0))
                leccion1 = float(request.form.get('NotaLeccion1', 0))
                examen1 = float(request.form.get('NotaExamen1', 0))
                promedio1 = round((autonoma1 + practica1 + leccion1 + examen1) / 4, 2)

                calif.NotaAutonoma1 = autonoma1
                calif.NotaPractica1 = practica1
                calif.NotaLeccion1 = leccion1
                calif.NotaExamen1 = examen1
                calif.PromQuimestre1 = promedio1
                
                autonoma2 = float(request.form.get('NotaAutonoma2', 0))
                practica2 = float(request.form.get('NotaPractica2', 0))
                leccion2 = float(request.form.get('NotaLeccion2', 0))
                examen2 = float(request.form.get('NotaExamen2', 0))
                promedio2 = round((autonoma2 + practica2 + leccion2 + examen2) / 4, 2)

                calif.NotaAutonoma2 = autonoma2
                calif.NotaPractica2 = practica2
                calif.NotaLeccion2 = leccion2
                calif.NotaExamen2 = examen2
                calif.PromQuimestre2 = promedio2

                q1 = calif.PromQuimestre1 or 0
                q2 = calif.PromQuimestre2 or 0
                calif.PromedioFinal = round((q1 + q2) / 2, 2)

                id_matricula = db.session.query(MatriculaAsignacion.idMatricula).filter_by(idMatriculaAsignacion=id_matricula_asignacion).scalar()
                self.actualizar_promedio_anual(id_matricula=id_matricula)
                
                db.session.commit()
                return { 'mensaje': ('Calificación actualizada correctamente', 'successful') }

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al actualizar calificación: {e}')
                return { 'mensaje': ('No se pudo actualizar la calificación', 'danger') }

    def delete_calificacion(self, id_matricula_asignacion):
        try:
            calif = Calificacion.query.filter_by(idMatriculaAsignacion=id_matricula_asignacion).first()
            if not calif:
                return { 'mensaje': ('No se encontró la calificación para eliminar', 'info') }

            db.session.delete(calif)
            db.session.commit()
            return { 'mensaje': ('Calificación eliminada correctamente', 'successfuls') }
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar calificación: {e}')
            return { 'mensaje': ('No se pudo eliminar la calificación', 'danger') }

        
    def get_asignaciones_por_estudiante(self, id_estudiante):
        try:
            asignaciones = db.session.query(
                MatriculaAsignacion.idMatriculaAsignacion,
                AsignacionCurso.idCursoAsignacion,
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
                    'idCursoAsignacion': a.idCursoAsignacion,
                    'materia': a.nombre_materia,
                    'profesor': f'{a.nombre_profesor} {a.apellido_profesor}',
                    'nivel': a.Nivel,
                    'paralelo': a.Paralelo
                })

            return resultado
        except SQLAlchemyError as e:
            print(f' * Error al obtener asignaciones del estudiante: {e}')
            return []
    
    def actualizar_promedio_anual(self, id_matricula):
        promedio = db.session.query(
            func.avg(Calificacion.PromedioFinal)
        ).filter_by(idMatricula=id_matricula).scalar()

        matricula = db.session.get(Matricula, id_matricula)
        matricula.PromedioAnual = float(promedio) if promedio is not None else 0.0
        db.session.commit()
