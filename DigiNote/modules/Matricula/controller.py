# controller.py
from DigiNote.database.db import mysql
from ..Estudiante.controller import EstudianteController
from ..Curso.controller import CursoController
from ..Calificaciones.controller import CalificacionesController

class MatriculaController:
    def __init__(self):
        self.estudiante = EstudianteController()
        self.curso = CursoController()
        self.calificacion = CalificacionesController()

    def show_matricula(self):
        # Datos de la matrícula
        cur1 = mysql.connection.cursor()
        cur1.execute("""
            SELECT 
                M.idMatricula,
                CONCAT(E.Apellido, ' ', E.Nombre) AS Estudiante,
                M.FechaMatricula,
                M.Nivel,
                M.PromedioAnual
            FROM Matricula M
            JOIN Estudiante E ON M.idEstudiante = E.idEstudiante
        """)
        matriculas = cur1.fetchall()
        cur1.close()

       # Materias inscritas por matrícula       
        cur2 = mysql.connection.cursor()
        cur2.execute("""
            SELECT 
                MA.idMatricula,
                Matr.Nombre AS Materia,
                AC.Paralelo,
                CONCAT(P.Apellido, ' ', P.Nombre) AS Profesor
            FROM MatriculaAsignacion MA
            JOIN AsignacionCurso AC ON MA.idAsignacion = AC.idAsignacion
            JOIN Materia Matr ON AC.idMateria = Matr.idMateria
            JOIN Profesor P ON AC.idProfesor = P.idProfesor
            JOIN PeriodoLectivo Prd ON AC.idPeriodo = Prd.idPeriodo
            WHERE Prd.Estado = 'Activo'
        """)
        asignaciones = cur2.fetchall()
        cur2.close()
        return (matriculas, asignaciones)


    def add_matricula(self, request):
        if request.method == 'POST':
            idEstudiante = request.form['idEstudiante']
            asignaciones = request.form.getlist('idAsignacion')
            fechaMatricula = request.form['FechaMatricula']
            nivel = request.form['Nivel']
            promedio = request.form.get('PromedioAnual', 0)

            try:
                cur = mysql.connection.cursor()
                # Insertar matrícula
                cur.execute("""
                    INSERT INTO Matricula (idEstudiante, FechaMatricula, Nivel, PromedioAnual)
                    VALUES (%s, %s, %s, %s)
                """, (idEstudiante, fechaMatricula, nivel, promedio))
                idMatricula = cur.lastrowid

                # Insertar asignaciones de cursos por matricula
                for idAsignacion in asignaciones:
                    cur.execute("""
                        INSERT INTO MatriculaAsignacion (idMatricula, idAsignacion)
                        VALUES (%s, %s)
                    """, (idMatricula, idAsignacion))

                mysql.connection.commit()
                cur.close()
                return ('Matrícula creada correctamente con sus asignaciones.', 'successful')

            except Exception as e:
                print(f'Error en add_matricula: {e}')
                return ('ERROR: No se pudo registrar la matrícula.', 'error')


    def get_matricula_by_id(self, id):
        cur1 = mysql.connection.cursor()
        cur1.execute("""
            SELECT idMatricula, idEstudiante, FechaMatricula, Nivel, PromedioAnual
            FROM Matricula
            WHERE idMatricula = %s
        """, (id,))
        matricula = cur1.fetchone()
        cur1.close()
        
        # Obtener las asignaciones asociadas a la matrícula
        cur2 = mysql.connection.cursor()
        cur2.execute("""
            SELECT idAsignacion
            FROM MatriculaAsignacion
            WHERE idMatricula = %s
        """, (id,))
        asignaciones = [row['idAsignacion'] for row in cur2.fetchall()]

        cur2.close()

        if matricula:
            matricula['asignaciones'] = asignaciones
            return matricula
        else:
            return {}

    def update_matricula(self, id, request):
        if request.method == 'POST':
            idEstudiante = request.form['idEstudiante']
            fechaMatricula = request.form['FechaMatricula']
            nivel = request.form['Nivel']
            nuevas_asignaciones = request.form.getlist('idAsignacion')
            promedio = self.calificacion.promedioAnual()

            try:
                cur = mysql.connection.cursor()

                # Actualizar datos básicos
                cur.execute("""
                    UPDATE Matricula
                    SET idEstudiante = %s,
                        FechaMatricula = %s,
                        Nivel = %s,
                        PromedioAnual = %s
                    WHERE idMatricula = %s
                """, (idEstudiante, fechaMatricula, nivel, promedio, id))

                # Obtener asignaciones actuales
                cur.execute("SELECT idAsignacion FROM MatriculaAsignacion WHERE idMatricula = %s", (id,))
                asig_actual = [str(row['idAsignacion']) for row in cur.fetchall()]

                # Eliminar asignaciones quitadas
                for id_asig in asig_actual:
                    if id_asig not in nuevas_asignaciones:
                        cur.execute("DELETE FROM MatriculaAsignacion WHERE idMatricula = %s AND idAsignacion = %s", (id, id_asig))

                # Insertar asignaciones añadidas
                for id_asig in nuevas_asignaciones:
                    if id_asig not in asig_actual:
                        cur.execute("INSERT INTO MatriculaAsignacion (idMatricula, idAsignacion) VALUES (%s, %s)", (id, id_asig))

                mysql.connection.commit()
                cur.close()
                return ('Matrícula actualizada correctamente', 'info')

            except Exception as e:
                print(f'Error al actualizar matrícula: {e}')
                return ('ERROR: No se pudo actualizar la matrícula.', 'error')



    def delete_matricula(self, id):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM MatriculaAsignacion WHERE idMatricula = %s', (id,))
        cur.execute('DELETE FROM Matricula WHERE idMatricula = %s', (id,))
        mysql.connection.commit()
        eliminado = cur.rowcount == 0
        cur.close()
        if eliminado:
            return ('No se encontró la matrícula para eliminar', 'info')
        return ('Matrícula eliminada correctamente', 'successful')

    def foreign_records(self):
        return {
            'estudiantes': self.estudiante.list_estudiantes(),
            'asignaciones': self.curso.list_curso()
        }


