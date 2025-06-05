from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import ProfesorController

profesor_bp = Blueprint('profesor', __name__, template_folder='DigiNote/templates')
controller = ProfesorController()

@profesor_bp.route('/')
def show():
    result = controller.show_profesor()
    return render_template(
        'profesor.html', 
        registros=result,
        active_page='prof',
        r_add=url_for('profesor.add'),
        r_get=url_for('profesor.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('profesor.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('profesor.delete', id=0).rsplit('/', 1)[0]
    )

@profesor_bp.route('/add_profesor', methods=['POST'])
def add():
    result = controller.add_profesor(request)
    flash(*result)
    return redirect(url_for('profesor.show'))

@profesor_bp.route('/get_profesor/<int:id>', methods=['GET', 'POST'])
def get(id):
    profesor = controller.get_profesor_by_id(id)
    if profesor:
        return jsonify({
            'Cedula': profesor.Cedula,
            'Nombre': profesor.Nombre,
            'Apellido': profesor.Apellido,
            'Telefono': profesor.Telefono,
            'Especialidad': profesor.Especialidad,
            'Direccion': profesor.Direccion
        })
    return jsonify({}), 404

@profesor_bp.route('/update_profesor/<int:id>', methods=['POST'])
def update(id):
    result = controller.update_profesor(id, request)
    flash(*result)
    return redirect(url_for('profesor.show'))

@profesor_bp.route('/delete_profesor/<int:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_profesor(id)
    flash(*result)
    return redirect(url_for('profesor.show'))
