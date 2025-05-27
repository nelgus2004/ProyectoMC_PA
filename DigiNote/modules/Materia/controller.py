from DigiNote.database.db import mysql

class MateriaController:
    def show_materia(self):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Materia')
        data = cur.fetchall()
        cur.close()
        return data

    def add_materia(self, request):
        if request.method == 'POST':
            nombre = request.form['Nombre'].strip().title()
            nivel = request.form['Nivel']
            descripcion = request.form.get('Descripcion') or None
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO Materia (Nombre, Nivel, Descripcion)
                    VALUES (%s, %s, %s)
                """, (nombre, nivel, descripcion))
                mysql.connection.commit()
                cur.close()
                return ('Materia añadida correctamente', 'successful')
            except Exception as e:
                print(f'Error al añadir materia: {e}')
                return ('ERROR: No se pudo añadir la materia.', 'error')

    def get_materia_by_id(self, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Materia WHERE idMateria = %s', (id,))
        data = cur.fetchall()
        cur.close()
        if data:
            return data[0]
        return None

    def update_materia(self, id, request):
        if request.method == 'POST':
            nombre = request.form['Nombre'].strip().title()
            nivel = request.form['Nivel']
            descripcion = request.form.get('Descripcion') or None
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    UPDATE Materia
                    SET Nombre = %s,
                        Nivel = %s,
                        Descripcion = %s
                    WHERE idMateria = %s
                """, (nombre, nivel, descripcion, id))
                mysql.connection.commit()
                cur.close()
                return ('Materia editada correctamente', 'info')
            except Exception as e:
                print(f'Error al editar materia: {e}')
                return ('ERROR: No se pudo editar la materia.', 'error')

    def delete_materia(self, id):
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM Materia WHERE idMateria = %s', (id,))
            mysql.connection.commit()
            eliminado = cur.rowcount == 0
            cur.close()
            if eliminado:
                return ('No se encontró la materia para eliminar', 'info')
            return ('Materia eliminada correctamente', 'successful')
        except Exception as e:
            print(f'Error al eliminar materia: {e}')
            return ('ERROR: No se pudo eliminar la materia.', 'error')

    def list_materias(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT idMateria, Nombre, Nivel FROM Materia")
        data = cur.fetchall()
        cur.close()
        return data
