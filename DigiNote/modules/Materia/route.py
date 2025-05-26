from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import MateriaController

materia_bp = Blueprint('materia', __name__, template_folder='DigiNote/templates')
controller = MateriaController()

@materia_bp.route('/')
def show():
    result = controller.show_materia()
    return render_template(
        'materia.html', 
        registros=result, 
        active_page='mat', 
        r_get=url_for('materia.get', id='').rstrip('/'),
        r_update=url_for('materia.update', id='').rstrip('/'),
        campos=['Nombre', 'Nivel', 'Descripcion']
    )

@materia_bp.route('/add_materia', methods=['POST'])
def add():
    result = controller.add_materia(request)
    flash(*result)
    return redirect(url_for('materia.show'))

@materia_bp.route('/get_materia/<id>', methods=['POST', 'GET'])
def get(id):
    result = controller.get_materia_by_id(id)
    return jsonify(result)

@materia_bp.route('/update_materia/<id>', methods=['POST'])
def update(id):
    result = controller.update_materia(id, request)
    flash(*result)
    return redirect(url_for('materia.show'))

@materia_bp.route('/delete_materia/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_materia(id)
    flash(*result)
    return redirect(url_for('materia.show'))
