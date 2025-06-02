from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import Profesor

class ProfesorController:
    def show_profesor(self):
        return Profesor.query.all()

    def add_profesor(self, request):
        if request.method == 'POST':
            cedula = request.form['Cedula']
            nombre = request.form['Nombre'].strip().title()
            apellido = request.form['Apellido'].strip().title()
            telefono = request.form.get('Telefono') or None
            correo = request.form.get('Correo') or None
            especialidad = request.form.get('Esspecialidad') or None
            direccion = request.form.get('Direccion') or None

            try:
                nuevo = Profesor(
                    Cedula=cedula,
                    Nombre=nombre,
                    Apellido=apellido,
                    Telefono=telefono,
                    Correo=correo,
                    Especialidad=especialidad,
                    Direccion=direccion
                )
                db.session.add(nuevo)
                db.session.commit()
                return ('Profesor añadido correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al añadir profesor: {e}')
                return ('ERROR: No se pudo añadir al profesor.', 'error')

    def get_profesor_by_id(self, id):
        return Profesor.query.get(id)

    def update_profesor(self, id, request):
        if request.method == 'POST':
            try:
                profesor = Profesor.query.get(id)
                if not profesor:
                    return ('No se encontró el profesor.', 'error')

                profesor.Cedula = request.form['Cedula']
                profesor.Nombre = request.form['Nombre'].strip().title()
                profesor.Apellido = request.form['Apellido'].strip().title()
                profesor.Telefono = request.form.get('Telefono') or None
                profesor.Correo = request.form.get('Correo') or None
                profesor.Especialidad = request.form.get('Especialidad') or None
                profesor.Direccion = request.form.get('Direccion') or None

                db.session.commit()
                return ('Profesor editado correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al editar profesor: {e}')
                return ('ERROR: No se pudo editar al profesor.', 'error')

    def delete_profesor(self, id):
        try:
            profesor = Profesor.query.get(id)
            if not profesor:
                return ('No se encontró el profesor para eliminar.', 'info')

            db.session.delete(profesor)
            db.session.commit()
            return ('Profesor eliminado correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar profesor: {e}')
            return ('ERROR: No se pudo eliminar al profesor.', 'error')

    def list_profesores(self):
        return Profesor.query.with_entities(
            Profesor.idProfesor,
            Profesor.Nombre,
            Profesor.Apellido
        ).all()
