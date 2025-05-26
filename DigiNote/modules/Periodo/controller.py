from DigiNote.database.db import mysql

class PeriodoController:
    def show_periodo(self):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM PeriodoLectivo')
        data = cur.fetchall()
        cur.close()
        return data

    def add_periodo(self, request):
        if request.method == 'POST':
            nombre = request.form['Nombre']
            fecha_inicio = request.form['FechaInicio']
            fecha_fin = request.form['FechaFin']
            estado = request.form.get('Estado') or 'Inactivo'
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO PeriodoLectivo (Nombre, FechaInicio, FechaFin, Estado)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, fecha_inicio, fecha_fin, estado))
                mysql.connection.commit()
                cur.close()
                return ('Periodo añadido correctamente', 'successful')
            except Exception as e:
                print(f'Error al añadir periodo: {e}')
                return ('ERROR: No se pudo añadir el periodo.', 'error')

    def get_periodo_by_id(self, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM PeriodoLectivo WHERE idPeriodo = %s', (id,))
        data = cur.fetchall()
        cur.close()
        if data:
            return data[0]
        return None

    def update_periodo(self, id, request):
        if request.method == 'POST':
            nombre = request.form['Nombre']
            fecha_inicio = request.form['FechaInicio']
            fecha_fin = request.form['FechaFin']
            estado = request.form.get('Estado') or 'Inactivo'
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE PeriodoLectivo
                    SET Nombre = %s,
                        FechaInicio = %s,
                        FechaFin = %s,
                        Estado = %s
                    WHERE idPeriodo = %s
                """, (nombre, fecha_inicio, fecha_fin, estado, id))
                mysql.connection.commit()
                cur.close()
                return ('Periodo editado correctamente', 'info')
            except Exception as e:
                print(f'Error al editar periodo: {e}')
                return ('ERROR: No se pudo editar el periodo.', 'error')

    def delete_periodo(self, id):
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM PeriodoLectivo WHERE idPeriodo = %s', (id,))
            mysql.connection.commit()
            eliminado = cur.rowcount == 0
            cur.close()
            if eliminado:
                return ('No se encontró el periodo para eliminar', 'info')
            return ('Periodo eliminado correctamente', 'successful')
        except Exception as e:
            print(f'Error al eliminar periodo: {e}')
            return ('ERROR: No se pudo eliminar el periodo.', 'error')
