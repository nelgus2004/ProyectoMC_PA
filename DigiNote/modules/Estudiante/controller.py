from flask import request
from DigiNote.database import db
from DigiNote.database.models import Estudiante
from sqlalchemy.exc import SQLAlchemyError

class EstudianteController:
    def show_estudiante(self):
        return Estudiante.query.all()

    def add_estudiante(self, request):
        if request.method == 'POST':
            try:
                estudiante = Estudiante(
                    Cedula=request.form['Cedula'],
                    Nombre=request.form['Nombre'].strip().title(),
                    Apellido=request.form['Apellido'].strip().title(),
                    FechaNacimiento=request.form['FechaNacimiento'],
                    Correo=request.form['Correo'],
                    Telefono=request.form.get('Telefono'),
                    Direccion=request.form.get('Direccion', ''),
                    Observacion=request.form.get('Observacion')
                )
                db.session.add(estudiante)
                db.session.commit()
                return ('Estudiante añadido correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al añadir estudiante: {e}')
                return ('ERROR: No se pudo añadir al estudiante.', 'error')

    def get_estudiante_by_id(self, id):
        return Estudiante.query.get(id)

    def update_estudiante(self, id, request):
        if request.method == 'POST':
            try:
                estudiante = Estudiante.query.get(id)
                if not estudiante:
                    return ('Estudiante no encontrado', 'error')
                estudiante.Cedula = request.form['Cedula']
                estudiante.Nombre = request.form['Nombre'].strip().title()
                estudiante.Apellido = request.form['Apellido'].strip().title()
                estudiante.FechaNacimiento = request.form['FechaNacimiento']
                estudiante.Correo = request.form['Correo']
                estudiante.Telefono = request.form.get('Telefono')
                estudiante.Direccion = request.form.get('Direccion', '')
                estudiante.Observacion = request.form.get('Observacion')
                db.session.commit()
                return ('Estudiante editado correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al actualizar estudiante: {e}')
                return ('ERROR: No se pudo actualizar el estudiante.', 'error')

    def delete_estudiante(self, id):
        try:
            estudiante = Estudiante.query.get(id)
            if not estudiante:
                return ('No se encontró el estudiante para eliminar', 'info')
            db.session.delete(estudiante)
            db.session.commit()
            return ('Estudiante eliminado correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar estudiante: {e}')
            return ('ERROR: No se pudo eliminar el estudiante.', 'error')

    def list_estudiantes(self):
        return Estudiante.query.with_entities(
            Estudiante.idEstudiante,
            Estudiante.Cedula,
            Estudiante.Nombre,
            Estudiante.Apellido
        ).all()
