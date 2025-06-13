from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import MatriculaController
from datetime import date

matricula_bp = Blueprint('matricula', __name__, template_folder='DigiNote/templates')
controller = MatriculaController()

@matricula_bp.route('/')
def show():
    result = controller.show_matricula()
    foreign = controller.foreign_records() or ''
    fecha_actual = date.today().isoformat()

    return render_template(
        'matricula.html',
        registros=result['matriculas'],
        fecha_actual=fecha_actual,
        foraneo=foreign,
        active_page='matr',
        r_add=url_for('matricula.add'),
        r_get=url_for('matricula.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('matricula.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('matricula.delete', id=0).rsplit('/', 1)[0]
    )

@matricula_bp.route('/add_matricula', methods=['POST'])
def add():
    result = controller.add_matricula(request)
    flash(*result['mensaje'])
    return redirect(url_for('matricula.show'))

@matricula_bp.route('/get_matricula/<id>', methods=['GET'])
def get(id):
    result = controller.get_matricula_by_id(id)
    return jsonify(result)

@matricula_bp.route('/update_matricula/<id>', methods=['POST'])
def update(id):
    result = controller.update_matricula(id, request)
    flash(*result['mensaje'])
    return redirect(url_for('matricula.show'))

@matricula_bp.route('/delete_matricula/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_matricula(id)
    print(*result['mensaje'])
    flash(*result['mensaje'])
    return redirect(url_for('matricula.show'))
