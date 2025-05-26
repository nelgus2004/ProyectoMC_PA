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
        r_get=url_for('periodo.get', id='').rstrip('/'),
        r_update=url_for('periodo.update', id='').rstrip('/'),
        campos=['Nombre', 'FechaInicio', 'FechaFin', 'Estado']
    )

@periodo_bp.route('/add_periodo', methods=['POST'])
def add():
    result = controller.add_periodo(request)
    flash(*result)
    return redirect(url_for('periodo.show'))

@periodo_bp.route('/get_periodo/<id>', methods=['POST', 'GET'])
def get(id):
    result = controller.get_periodo_by_id(id)
    return jsonify(result)

@periodo_bp.route('/update_periodo/<id>', methods=['POST'])
def update(id):
    result = controller.update_periodo(id, request)
    flash(*result)
    return redirect(url_for('periodo.show'))

@periodo_bp.route('/delete_periodo/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_periodo(id)
    flash(*result)
    return redirect(url_for('periodo.show'))
