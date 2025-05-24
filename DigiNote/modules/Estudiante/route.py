from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from .controller import MainController

estudiante_bp = Blueprint('estudiante', __name__, template_folder='DigiNote/templates')
controller = MainController()

@estudiante_bp.route('/')
def show():
    result = controller.show_estudiante()
    return render_template(
        'estudiante.html', 
        registros = result, 
        active_page = 'est', 
        r_get = url_for('estudiante.get', id='').rstrip('/'),
        r_update = url_for('estudiante.update', id='').rstrip('/'), 
        campos = ['Cedula', 'Nombre', 'Apellido', 'FechaNacimiento', 'Correo', 'Telefono', 'Direccion', 'Observacion'])

@estudiante_bp.route('/add_estudiante', methods=['POST'])
def add():
    result = controller.add_estudiante(request)
    print(result)
    return redirect(url_for('estudiante.show'))

@estudiante_bp.route('/get_estudiante/<id>', methods=['POST', 'GET'])
def get(id):
    result = controller.get_estudiante_by_id(id)
    return jsonify(result)

@estudiante_bp.route('/update_estudiante/<id>', methods=['POST'])
def update(id):
    result = controller.update_estudiante(id, request)
    print(result)
    return redirect(url_for('estudiante.show'))

@estudiante_bp.route('/delete_estudiante/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_estudiante(id)
    print(result)
    return redirect(url_for('estudiante.show'))
