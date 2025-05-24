from DigiNote.database.db import mysql

class MainController:
    def show_estudiante(self):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM estudiante')
        data = cur.fetchall()
        cur.close()        
        return data
    
    def add_estudiante(self, request):
        if request.method == 'POST':
            cedula = request.form['Cedula']
            nombre = request.form['Nombre']
            apellido = request.form['Apellido']
            fechaNacimiento = request.form['FechaNacimiento']
            correo = request.form['Correo']
            telefono = request.form['Telefono'] or None
            direccion = request.form['Direccion'] or None
            observacion = request.form['Observacion'] or None
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                    INSERT INTO Estudiante (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (cedula, nombre, apellido, fechaNacimiento, correo, telefono, direccion, observacion))
            mysql.connection.commit()
            return 'Estudiante Añadido Correctamente'
        except Exception as e:
            print(f'Error al añadir estudiante: {e}')
            return 'ERROR: No se pudo añadir al estudiante.'
        
    def get_estudiante_by_id(self, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Estudiante WHERE idEstudiante = %s', (id,))
        data = cur.fetchall()
        cur.close()
        #print(data[0])
        return data[0]

    def update_estudiante(self, id, request):
        if request.method == 'POST':
            cedula = request.form['Cedula']
            nombre = request.form['Nombre']
            apellido = request.form['Apellido']
            fechaNacimiento = request.form['FechaNacimiento']
            correo = request.form['Correo']
            telefono = request.form['Telefono'] or None
            direccion = request.form['Direccion'] or None
            observacion = request.form['Observacion'] or None
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE Estudiante
                SET Cedula = %s,
                    Nombre = %s,
                    Apellido = %s,
                    FechaNacimiento = %s,
                    Correo = %s,
                    Telefono = %s,
                    Direccion = %s,
                    Observacion = %s
                WHERE idEstudiante = %s
            """, (cedula, nombre, apellido, fechaNacimiento, correo, telefono, direccion, observacion, id))
            mysql.connection.commit()
            cur.close()
            return 'Estudiante Editado Correctamente'

    def delete_estudiante(self, id):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Estudiante WHERE idEstudiante = %s', (id,))
        mysql.connection.commit()
        eliminado = cur.rowcount == 0
        cur.close()
        if eliminado:
            return 'No se encontró el estudiante para eliminar.'
        return 'Estudiante Eliminado Correctamente'
