from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func 
from DigiNote.database import db
from DigiNote.database.models import Estudiante, Materia, Matricula, MatriculaAsignacion, Profesor, Curso, AsignacionCurso, PeriodoLectivo, Calificacion
from datetime import date

class MatriculaController:
    def __init__(self):
        pass

    def show_matricula(self):
        try:
            # Consulta de matrículas activas
            matriculas = db.session.query(
                Matricula.idMatricula,
                Estudiante.Apellido,
                Estudiante.Nombre,
                Estudiante.Cedula,
                Matricula.FechaMatricula,
                Matricula.Nivel,
                Matricula.Paralelo,
                Matricula.PromedioAnual
            ).join(Estudiante, Estudiante.idEstudiante == Matricula.idEstudiante) \
            .join(PeriodoLectivo, PeriodoLectivo.idPeriodo == Matricula.idPeriodo) \
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .all()
            

            # Consulta de asignaciones para matrículas activas
            asignaciones = db.session.query(
                MatriculaAsignacion.idMatricula,
                Materia.Nombre.label('materia'),
                Curso.Paralelo,
                Curso.Nivel,
                Profesor.Apellido.label('profesor_apellido'),
                Profesor.Nombre.label('profesor_nombre')
            ).join(AsignacionCurso, AsignacionCurso.idCursoAsignacion == MatriculaAsignacion.idCursoAsignacion) \
            .join(Materia, Materia.idMateria == AsignacionCurso.idMateria) \
            .join(Profesor, Profesor.idProfesor == AsignacionCurso.idProfesor) \
            .join(Curso, Curso.idCurso == AsignacionCurso.idCurso) \
            .join(PeriodoLectivo, PeriodoLectivo.idPeriodo == AsignacionCurso.idPeriodo) \
            .filter(PeriodoLectivo.Estado == 'Activo') \
            .all()
            

            asignaciones_dict = {}
            for asign in asignaciones:
                if asign.idMatricula not in asignaciones_dict:
                    asignaciones_dict[asign.idMatricula] = []
                asignaciones_dict[asign.idMatricula].append({
                    'materia': asign.materia,
                    'paralelo': asign.Paralelo,
                    'nivel': asign.Nivel,
                    'profesor': f"{asign.profesor_nombre} {asign.profesor_apellido}"
                })

            resultado = []
            for mat in matriculas:
                matricula = {
                    'idMatricula': mat.idMatricula,
                    'cedula': mat.Cedula,
                    'estudiante': f"{mat.Apellido} {mat.Nombre}",
                    'fecha_matricula': mat.FechaMatricula.strftime('%Y-%m-%d'),
                    'nivel': mat.Nivel,
                    'paralelo': mat.Paralelo,
                    'promedio_anual': float(mat.PromedioAnual) if mat.PromedioAnual else 0.0,
                    'asignaciones': asignaciones_dict.get(mat.idMatricula, [])
                }
                resultado.append(matricula)

            return {'matriculas': resultado}

        except SQLAlchemyError as e:
            print(f"Error al obtener matrículas: {e}")
            return {'matriculas': []}
    
         
    def add_matricula(self, request):
        if request.method == 'POST':
            periodo_activo = db.session.query(PeriodoLectivo).filter_by(Estado='Activo').first()
            try:
                nueva = Matricula(
                    idEstudiante=request.form['idEstudiante'],
                    FechaMatricula=request.form.get('FechaMatricula', date.today()),
                    Nivel=request.form['Nivel'],
                    Paralelo=request.form['Paralelo'],
                    PromedioAnual=request.form.get('PromedioAnual', 0),
                    idPeriodo= periodo_activo.idPeriodo 
                )

                db.session.add(nueva)
                db.session.flush()

                for id_asig in request.form.getlist('idCursoAsignacion'):
                    nueva_asignacion = MatriculaAsignacion(idMatricula=nueva.idMatricula, idCursoAsignacion=id_asig)
                    db.session.add(nueva_asignacion)
                    db.session.flush()
                    
                    # Crear el registro de calificación con valores en 0
                    nueva_calificacion = Calificacion(
                        idMatricula=nueva.idMatricula,
                        idMatriculaAsignacion=nueva_asignacion.idMatriculaAsignacion,
       
                    )
                    db.session.add(nueva_calificacion)
                db.session.commit()
                
                return { 'mensaje': ('Matrícula creada correctamente con sus asignaciones', 'successful') } 
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error en add_matricula: {e}")
                return { 'mensaje': ('No se pudo registrar la matrícula', 'danger') } 
            

    def get_matricula_by_id(self, id):
        try:
            matricula = db.session.get(Matricula, id)
            if not matricula:
                return []

            asignaciones = [ma.idCursoAsignacion for ma in matricula.matricula_asignacion]
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
            return []

    def update_matricula(self, id, request):
        if request.method == 'POST':
            try:
                matricula = db.session.get(Matricula, id)
                periodo_activo = db.session.query(PeriodoLectivo).filter_by(Estado='Activo').first()
                if not matricula:
                    return { 'mensaje': ('Matrícula no encontrada', 'danger') } 

                matricula.idEstudiante = request.form['idEstudiante']
                matricula.FechaMatricula = request.form.get('FechaMatricula', matricula.FechaMatricula)
                matricula.Nivel = request.form['Nivel']
                matricula.Paralelo=request.form['Paralelo']
                matricula.PromedioAnual = request.form.get('PromedioAnual', matricula.PromedioAnual)
                matricula.idPeriodo = periodo_activo.idPeriodo 
                
                # Procesar asignaciones
                nuevas_asignaciones = set(request.form.getlist('idCursoAsignacion'))
                actuales_asignaciones = {str(ma.idCursoAsignacion) for ma in matricula.matricula_asignacion}

                eliminar = actuales_asignaciones - nuevas_asignaciones
                agregar = nuevas_asignaciones - actuales_asignaciones
                
                # Eliminar las que ya no están
                for ma in list(matricula.matricula_asignacion):
                    if str(ma.idCursoAsignacion) in eliminar:
                        db.session.query(Calificacion).filter_by(
                            idMatriculaAsignacion=ma.idMatriculaAsignacion
                        ).delete()
                        db.session.delete(ma)

                # Añadir las nuevas
                for id_asig in agregar:
                    nueva_asignacion = MatriculaAsignacion(
                        idMatricula=id,
                        idCursoAsignacion=id_asig
                    )
                    db.session.add(nueva_asignacion)
                    db.session.flush()
                    
                    nueva_calificacion = Calificacion(
                        idMatricula=id,
                        idMatriculaAsignacion=nueva_asignacion.idMatriculaAsignacion
                    )
                    db.session.add(nueva_calificacion)

                db.session.commit()
                return { 'mensaje': ('Matrícula actualizada correctamente', 'info') } 
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al actualizar matrícula: {e}")
                return { 'mensaje': ('No se pudo actualizar la matrícula', 'danger') } 


    def delete_matricula(self, id):
        try:
            matricula = db.session.get(Matricula, id)
            if not matricula:
                return { 'mensaje': ('No se encontró la matrícula para eliminar', 'info') }
                                    
            db.session.delete(matricula)
            db.session.commit()
            return ('Matrícula eliminada correctamente', 'danger')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar matrícula: {e}")
            return { 'mensaje': ('No se pudo eliminar la matrícula', 'danger') } 
        

    def foreign_records(self):
        try:
            estudiantes = db.session.query(
                Estudiante.idEstudiante,
                Estudiante.Nombre,
                Estudiante.Apellido
            ).all()

            asignaciones = db.session.query(
                AsignacionCurso.idCursoAsignacion,
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
                    "idCursoAsignacion": asig.idCursoAsignacion,
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
            return { 'estudiantes': [],  'asignaciones': [] }