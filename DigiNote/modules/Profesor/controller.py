from DigiNote.database.db import mysql

class ProfesorController:
    def show_profesor(self):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Profesor')
        data = cur.fetchall()
        cur.close()
        return data

    def add_profesor(self, request):
        if request.method == 'POST':
            cedula = request.form['Cedula']
            nombre = request.form['Nombre']
            apellido = request.form['Apellido']
            telefono = request.form['Telefono'] or None
            correo = request.form['Correo'] or None
            especialidad = request.form['Especialidad'] or None
            direccion = request.form['Direccion'] or None
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO Profesor (Cedula, Nombre, Apellido, Telefono, Correo, Especialidad, Direccion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cedula, nombre, apellido, telefono, correo, especialidad, direccion))
                mysql.connection.commit()
                return ('Profesor Añadido Correctamente', 'successful')
            except Exception as e:
                print(f'Error al añadir profesor: {e}')
                return ('ERROR: No se pudo añadir al profesor.', 'error')

    def get_profesor_by_id(self, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Profesor WHERE idProfesor = %s', (id,))
        data = cur.fetchall()
        cur.close()
        return data[0] if data else {}

    def update_profesor(self, id, request):
        if request.method == 'POST':
            cedula = request.form['Cedula']
            nombre = request.form['Nombre']
            apellido = request.form['Apellido']
            telefono = request.form['Telefono'] or None
            correo = request.form['Correo'] or None
            especialidad = request.form['Especialidad'] or None
            direccion = request.form['Direccion'] or None

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE Profesor
                SET Cedula = %s,
                    Nombre = %s,
                    Apellido = %s,
                    Telefono = %s,
                    Correo = %s,
                    Especialidad = %s,
                    Direccion = %s
                WHERE idProfesor = %s
            """, (cedula, nombre, apellido, telefono, correo, especialidad, direccion, id))
            mysql.connection.commit()
            cur.close()
            return ('Profesor Editado Correctamente', 'info')

    def delete_profesor(self, id):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Profesor WHERE idProfesor = %s', (id,))
        mysql.connection.commit()
        eliminado = cur.rowcount == 0
        cur.close()
        if eliminado:
            return ('No se encontró el profesor para eliminar.', 'info')
        return ('Profesor Eliminado Correctamente', 'successful')

