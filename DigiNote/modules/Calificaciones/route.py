from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import CalificacionesController

calificacion_bp = Blueprint('calificacion', __name__, template_folder='DigiNote/templates')
controller = CalificacionesController()

@calificacion_bp.route('/')
def show():
    registros = controller.show_calificaciones()
    return render_template(
        'calificacion.html',
        registros=registros,
        active_page='calificacion',
        r_add=url_for('calificacion.add'),
        r_get=url_for('calificacion.get', id=0).rsplit('/', 1)[0],
        r_update=url_for('calificacion.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('calificacion.delete', id=0).rsplit('/', 1)[0]
    )

@calificacion_bp.route('/add', methods=['POST'])
def add():
    resultado = controller.add_calificacion(request)
    flash(*resultado)
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/get/<int:id>', methods=['GET'])
def get(id):
    resultado = controller.get_calificacion_by_id(id)
    return jsonify(resultado)

@calificacion_bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    resultado = controller.update_calificacion(id, request)
    flash(*resultado)
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    resultado = controller.delete_calificacion(id)
    flash(*resultado)
    return redirect(url_for('calificacion.show'))
