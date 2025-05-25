from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, make_response
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
        r_get=url_for('profesor.get', id='').rstrip('/'),
        r_update=url_for('profesor.update', id='').rstrip('/'),
        campos=['Cedula', 'Nombre', 'Apellido', 'Telefono', 'Correo', 'Especialidad', 'Direccion']
    )

@profesor_bp.route('/add_profesor', methods=['POST'])
def add():
    result = controller.add_profesor(request)
    flash(*result)
    return redirect(url_for('profesor.show'))

@profesor_bp.route('/get_profesor/<id>', methods=['POST', 'GET'])
def get(id):
    result = controller.get_profesor_by_id(id)
    return jsonify(result)

@profesor_bp.route('/update_profesor/<id>', methods=['POST'])
def update(id):
    result = controller.update_profesor(id, request)
    flash(*result)
    return redirect(url_for('profesor.show'))

@profesor_bp.route('/delete_profesor/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_profesor(id)
    flash(*result)
    return redirect(url_for('profesor.show'))
