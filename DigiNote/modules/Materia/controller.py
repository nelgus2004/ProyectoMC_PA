from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import Materia

class MateriaController:
    def show_materia(self):
        return Materia.query.all()

    def add_materia(self, request):
        if request.method == 'POST':
            try:
                materia = Materia(
                    Nombre=request.form['Nombre'].strip().title(),
                    Nivel=request.form['Nivel'],
                    Descripcion=request.form.get('Descripcion') or None
                )
                db.session.add(materia)
                db.session.commit()
                return ('Materia añadida correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al añadir materia: {e}")
                return ('ERROR: No se pudo añadir la materia.', 'error')

    def get_materia_by_id(self, id):
        return Materia.query.get(id)

    def update_materia(self, id, request):
        if request.method == 'POST':
            try:
                materia = Materia.query.get(id)
                if not materia:
                    return ('Materia no encontrada', 'info')
                materia.Nombre = request.form['Nombre'].strip().title()
                materia.Nivel = request.form['Nivel']
                materia.Descripcion = request.form.get('Descripcion') or None
                db.session.commit()
                return ('Materia editada correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al editar materia: {e}")
                return ('ERROR: No se pudo editar la materia.', 'error')

    def delete_materia(self, id):
        try:
            materia = Materia.query.get(id)
            if not materia:
                return ('No se encontró la materia para eliminar', 'info')
            db.session.delete(materia)
            db.session.commit()
            return ('Materia eliminada correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar materia: {e}")
            return ('ERROR: No se pudo eliminar la materia.', 'error')

    def list_materias(self):
        return Materia.query.with_entities(
            Materia.idMateria,
            Materia.Nombre,
            Materia.Nivel
        ).all()
