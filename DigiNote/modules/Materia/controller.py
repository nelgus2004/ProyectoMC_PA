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
                    Descripcion=request.form.get('Descripcion') or None
                )
                db.session.add(materia)
                db.session.commit()
                return { 'mensaje': ('Materia añadida correctamente', 'successful') }
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al añadir materia: {e}")
                return { 'mensaje': ('No se pudo añadir la materia', 'danger') }

    def get_materia_by_id(self, id):
        return Materia.query.get(id)

    def update_materia(self, id, request):
        if request.method == 'POST':
            try:
                materia = Materia.query.get(id)
                if not materia:
                    return { 'mensaje': ('Materia no encontrada', 'info') }
                materia.Nombre = request.form['Nombre'].strip().title()
                materia.Descripcion = request.form.get('Descripcion') or None
                db.session.commit()
                return { 'mensaje': ('Materia editada correctamente', 'info') }
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f" * Error al editar materia: {e}")
                return { 'mensaje': ('ERROR: No se pudo editar la materia.', 'danger') }

    def delete_materia(self, id):
        try:
            materia = Materia.query.get(id)
            if not materia:
                return { 'mensaje': ('No se encontró la materia para eliminar', 'info') }
            db.session.delete(materia)
            db.session.commit()
            return { 'mensaje': ('Materia eliminada correctamente', 'successful') }
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" * Error al eliminar materia: {e}")
            return { 'mensaje': ('No se pudo eliminar la materia.', 'danger') }
