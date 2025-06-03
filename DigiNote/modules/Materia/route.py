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
        r_add=url_for('materia.add'),
        r_get=url_for('materia.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('materia.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('materia.delete', id=0).rsplit('/', 1)[0]
    )

@materia_bp.route('/add_materia', methods=['POST'])
def add():
    result = controller.add_materia(request)
    flash(*result)
    return redirect(url_for('materia.show'))

@materia_bp.route('/get_materia/<int:id>', methods=['GET'])
def get(id):
    result = controller.get_materia_by_id(id)
    if result:
        return jsonify({
            'idMateria': result.idMateria,
            'Nombre': result.Nombre,
            'Descripcion': result.Descripcion
        })
    else:
        return jsonify({'error': 'Materia no encontrada'}), 404

@materia_bp.route('/update_materia/<int:id>', methods=['POST'])
def update(id):
    result = controller.update_materia(id, request)
    flash(*result)
    return redirect(url_for('materia.show'))

@materia_bp.route('/delete_materia/<int:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_materia(id)
    flash(*result)
    return redirect(url_for('materia.show'))
