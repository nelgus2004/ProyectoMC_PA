from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import EstudianteController

estudiante_bp = Blueprint('estudiante', __name__, template_folder='DigiNote/templates')
controller = EstudianteController()

@estudiante_bp.route('/')
def show():
    result = controller.show_estudiante()
    return render_template(
        'estudiante.html',
        registros=result,
        active_page='est',
        r_add=url_for('estudiante.add'),
        r_get=url_for('estudiante.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('estudiante.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('estudiante.delete', id=0).rsplit('/', 1)[0]
    )

@estudiante_bp.route('/add_estudiante', methods=['POST'])
def add():
    result = controller.add_estudiante(request)
    flash(*result)
    return redirect(url_for('estudiante.show'))

@estudiante_bp.route('/get_estudiante/<int:id>', methods=['GET'])
def get(id):
    result = controller.get_estudiante_by_id(id)
    if result:
        return jsonify({
            'idEstudiante': result.idEstudiante,
            'Cedula': result.Cedula,
            'Nombre': result.Nombre,
            'Apellido': result.Apellido,
            'FechaNacimiento': result.FechaNacimiento.isoformat(),
            'Correo': result.Correo,
            'Telefono': result.Telefono,
            'Direccion': result.Direccion,
            'Observacion': result.Observacion,
        })
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@estudiante_bp.route('/update_estudiante/<int:id>', methods=['POST'])
def update(id):
    result = controller.update_estudiante(id, request)
    flash(*result)
    return redirect(url_for('estudiante.show'))

@estudiante_bp.route('/delete_estudiante/<int:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_estudiante(id)
    flash(*result)
    return redirect(url_for('estudiante.show'))

