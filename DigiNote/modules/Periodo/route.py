from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import PeriodoController

periodo_bp = Blueprint('periodo', __name__, template_folder='DigiNote/templates')
controller = PeriodoController()

@periodo_bp.route('/')
def show():
    result = controller.show_periodo()
    return render_template(
        'periodo.html',
        registros=result,
        active_page='per',
        r_add=url_for('periodo.add'),
        r_get=url_for('periodo.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('periodo.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('periodo.delete', id=0).rsplit('/', 1)[0]
    )

@periodo_bp.route('/add_periodo', methods=['POST'])
def add():
    result = controller.add_periodo(request)
    flash(*result)
    return redirect(url_for('periodo.show'))

@periodo_bp.route('/get_periodo/<int:id>', methods=['GET'])
def get(id):
    result = controller.get_periodo_by_id(id)
    if result:
        return jsonify({
            'idPeriodo': result.idPeriodo,
            'Nombre': result.Nombre,
            'FechaInicio': result.FechaInicio.isoformat(),
            'FechaFin': result.FechaFin.isoformat(),
            'Estado': result.Estado,
        })
    else:
        return jsonify({'error': 'Periodo no encontrado'}), 404

@periodo_bp.route('/update_periodo/<int:id>', methods=['POST'])
def update(id):
    result = controller.update_periodo(id, request)
    flash(*result)
    return redirect(url_for('periodo.show'))

@periodo_bp.route('/delete_periodo/<int:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_periodo(id)
    flash(*result)
    return redirect(url_for('periodo.show'))
