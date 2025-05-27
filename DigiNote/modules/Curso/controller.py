from DigiNote.database.db import mysql
from ..Profesor.controller import ProfesorController
from ..Materia.controller import MateriaController
from ..Periodo.controller import PeriodoController
from datetime import timedelta


class CursoController:
    def __init__(self):
        self.profesor = ProfesorController()
        self.periodo = PeriodoController()
        self.materia = MateriaController()
        
    def show_curso(self):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT AC.idAsignacion, AC.Paralelo, AC.HoraEntrada, AC.HoraSalida, AC.Aula,
                CONCAT (P.Apellido, ' ', P.Nombre) AS Profesor,
                M.Nombre AS Materia, M.Nivel,
                CONCAT (PL.Nombre, ' ', DATE_FORMAT(FechaInicio, '%M'), '-' , DATE_FORMAT(FechaFin, '%M')) AS Periodo
            FROM AsignacionCurso AC
            JOIN Profesor P ON AC.idProfesor = P.idProfesor
            JOIN Materia M ON AC.idMateria = M.idMateria
            JOIN PeriodoLectivo PL ON AC.idPeriodo = PL.idPeriodo
            WHERE PL.Estado = 'Activo'
        """)
        data = cur.fetchall()
        cur.close()
        return data

    def add_curso(self, request):
        if request.method == 'POST':
            paralelo = request.form['Paralelo'].strip()
            horaEntrada = request.form['HoraEntrada']
            horaSalida = request.form['HoraSalida']
            aula = request.form['Aula'] or None
            idPeriodo = request.form['idPeriodo'] or None
            idProfesor = request.form['idProfesor'] or None
            idMateria = request.form['idMateria'] or None
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO AsignacionCurso (Paralelo, horaEntrada, horaSalida, Aula, idPeriodo, idProfesor, idMateria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (paralelo, horaEntrada, horaSalida, aula, idPeriodo, idProfesor, idMateria))
                mysql.connection.commit()
                return ('Curso Añadido Correctamente', 'successful')
            except Exception as e:
                print(f'Error al añadir curso: {e}')
                return ('ERROR: No se pudo añadir el curso.', 'error')

    def get_curso_by_id(self, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM AsignacionCurso WHERE idAsignacion = %s', (id,))
        data = cur.fetchall()
        cur.close()
        if not data:
            return {}
        curso = data[0]
        
        for campo in ['HoraEntrada', 'HoraSalida']:
            if isinstance(curso[campo], timedelta):  # Convertir timedelta a string HH:MM
                total_seconds = curso[campo].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                curso[campo] = f'{hours:02}:{minutes:02}'

        return curso

    def update_curso(self, id, request):
        if request.method == 'POST':
            paralelo = request.form['Paralelo'].strip()
            horaEntrada = request.form['HoraEntrada']
            horaSalida = request.form['HoraSalida']
            aula = request.form['Aula'] or None
            idPeriodo = request.form['idPeriodo'] or None
            idProfesor = request.form['idProfesor'] or None
            idMateria = request.form['idMateria'] or None
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE AsignacionCurso
                    SET Paralelo = %s,
                        horaEntrada = %s,
                        horaSalida = %s,
                        Aula = %s,
                        idPeriodo = %s,
                        idProfesor = %s,
                        idMateria = %s
                    WHERE idAsignacion = %s
                """, (paralelo, horaEntrada, horaSalida, aula, idPeriodo, idProfesor, idMateria, id))
                mysql.connection.commit()
                cur.close()
                return ('Curso Editado Correctamente', 'info')
            except Exception as e:
                print(f'Error al editar curso: {e}')
                return ('ERROR: No se pudo editar el curso.', 'error')

    def delete_curso(self, id):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM AsignacionCurso WHERE idAsignacion = %s', (id,))
        mysql.connection.commit()
        eliminado = cur.rowcount == 0
        cur.close()
        if eliminado:
            return ('No se encontró el curso para eliminar', 'info')
        return ('Curso Eliminado Correctamente', 'successful')
    
    def foreign_records(self):
        registros = {
            'profesores': self.profesor.list_profesores(),
            'materias': self.materia.list_materias(),
            'periodos': self.periodo.list_periodos()
        }
        return registros
    
    def list_curso(self):
        cur = mysql.connection.cursor()
        query = """
            SELECT 
                ac.idAsignacion,
                CONCAT(p.Nombre, ' ', p.Apellido) AS Profesor,
                m.Nombre AS Materia, m.Nivel,
                ac.Paralelo,
                pl.Nombre AS Periodo
            FROM AsignacionCurso ac
            JOIN Profesor p ON ac.idProfesor = p.idProfesor
            JOIN Materia m ON ac.idMateria = m.idMateria
            JOIN PeriodoLectivo pl ON ac.idPeriodo = pl.idPeriodo
            WHERE pl.Estado = 'Activo'
            ORDER BY pl.Nombre, ac.Paralelo, m.Nombre
        """
        cur.execute(query)
        resultados = cur.fetchall()
        cur.close()
        return resultados
