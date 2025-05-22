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
            telefono = request.form['Telefono']
            direccion = request.form['Direccion']
            observacion = request.form['Observacion']
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                    INSERT INTO Estudiante (Cedula, Nombre, Apellido, FechaNacimiento, Correo, Telefono, Direccion, Observacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (cedula, nombre, apellido, fechaNacimiento, correo, telefono, direccion, observacion))
            mysql.connection.commit()
            return 'Estudiante Añadido Correctamente'
        except Exception as e:
            return f'ERROR: No se pudo añadir al estudiante por \n {e}'