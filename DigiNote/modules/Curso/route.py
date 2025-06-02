from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import CursoController

curso_bp = Blueprint('curso', __name__, template_folder='DigiNote/templates')
controller = CursoController()

@curso_bp.route('/')
def show():
    result = controller.show_curso()
    foreign = controller.foreign_records()
    return render_template(
        'curso.html',
        registros=result,
        foraneo=foreign,
        active_page='cur',
        r_add=url_for('curso.add'),
        r_get=url_for('curso.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('curso.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('curso.delete', id=0).rsplit('/', 1)[0]
    )

@curso_bp.route('/add_curso', methods=['POST'])
def add():
    result = controller.add_curso(request)
    flash(*result)
    return redirect(url_for('curso.show'))

@curso_bp.route('/get_curso/<id>', methods=['GET', 'POST'])
def get(id):
    result = controller.get_curso_by_id(id)
    return jsonify(result)

@curso_bp.route('/update_curso/<id>', methods=['POST'])
def update(id):
    result = controller.update_curso(id, request)
    flash(*result)
    return redirect(url_for('curso.show'))

@curso_bp.route('/delete_curso/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_curso(id)
    flash(*result)
    return redirect(url_for('curso.show'))
