from flask import request
from sqlalchemy.exc import SQLAlchemyError
from DigiNote.database import db
from DigiNote.database.models import PeriodoLectivo

class PeriodoController:
    def show_periodo(self):
        return PeriodoLectivo.query.all()

    def add_periodo(self, request):
        if request.method == 'POST':
            try:
                estado = request.form.get('Estado') or 'Inactivo'
                if estado == 'Activo':
                    db.session.query(PeriodoLectivo).filter(PeriodoLectivo.Estado == 'Activo').update({'Estado': 'Inactivo'})
                
                periodo = PeriodoLectivo(
                    Nombre=request.form['Nombre'],
                    FechaInicio=request.form['FechaInicio'],
                    FechaFin=request.form['FechaFin'],
                    Estado=estado
                )
                db.session.add(periodo)
                db.session.commit()
                return ('Periodo añadido correctamente', 'successful')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al añadir periodo: {e}')
                return ('ERROR: No se pudo añadir el periodo.', 'error')

    def get_periodo_by_id(self, id):
        return PeriodoLectivo.query.get(id)

    def update_periodo(self, id, request):
        if request.method == 'POST':
            try:
                periodo = PeriodoLectivo.query.get(id)
                if not periodo:
                    return ('Periodo no encontrado', 'error')
                
                estado = request.form.get('Estado') or 'Inactivo'
                if estado == 'Activo':
                    db.session.query(PeriodoLectivo).filter(
                    PeriodoLectivo.Estado == 'Activo',
                    PeriodoLectivo.idPeriodo != id
                    ).update({'Estado': 'Inactivo'})
                
                periodo.Nombre = request.form['Nombre']
                periodo.FechaInicio = request.form['FechaInicio']
                periodo.FechaFin = request.form['FechaFin']
                periodo.Estado = estado
                db.session.commit()
                return ('Periodo editado correctamente', 'info')
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f' * Error al editar periodo: {e}')
                return ('ERROR: No se pudo editar el periodo.', 'error')

    def delete_periodo(self, id):
        try:
            periodo = PeriodoLectivo.query.get(id)
            if not periodo:
                return ('No se encontró el periodo para eliminar', 'info')
            db.session.delete(periodo)
            db.session.commit()
            return ('Periodo eliminado correctamente', 'successful')
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f' * Error al eliminar periodo: {e}')
            return ('ERROR: No se pudo eliminar el periodo.', 'error')

    def list_periodos(self):
        from sqlalchemy import func
        query = db.session.query(
            PeriodoLectivo.idPeriodo,
            PeriodoLectivo.Nombre,
            func.concat(
                func.date_format(PeriodoLectivo.FechaInicio, '%M'), '-',
                func.date_format(PeriodoLectivo.FechaFin, '%M')
            ).label('Duracion')
        ).filter(PeriodoLectivo.Estado == 'Activo')
        return query.all()
