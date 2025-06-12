from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import CalificacionesController

calificacion_bp = Blueprint('calificacion', __name__, template_folder='DigiNote/templates')
controller = CalificacionesController()

@calificacion_bp.route('/', methods=['GET'])
def show():
    result = controller.show_calificaciones()
    return render_template(
        'calificacion.html',
        registros=result,
        active_page='calif',
        r_add=url_for('calificacion.add'),
        r_get=url_for('calificacion.get_calificacion', id_estudiante=0).rsplit('/', 1)[0],
        r_update=url_for('calificacion.update', id_MatriculaAsignacion=0).rsplit('/', 1)[0],
        r_delete=url_for('calificacion.delete', id=0).rsplit('/', 1)[0],
        r_asignaciones=url_for('calificacion.obtener_asignaciones', id_estudiante=0).rsplit('/', 1)[0]
    )

@calificacion_bp.route('/add', methods=['POST'])
def add():
    result = controller.add_calificacion(request)
    flash(*result['mensaje'])
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/get/<int:id_estudiante>', methods=['GET'])
def get_calificacion(id_estudiante):
    result = controller.get_calificacion_by_id(id_estudiante=id_estudiante)
    flash(*result['mensaje'])
    if not result.get('resultado', {}):
        return jsonify({})
    return jsonify(result['resultado'])

@calificacion_bp.route('/update/<int:id_MatriculaAsignacion>', methods=['POST'])
def update(id_MatriculaAsignacion):
    print(f'hola {id_MatriculaAsignacion}')
    result = controller.update_calificacion(id_MatriculaAsignacion, request)
    flash(*result['mensaje'])
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_calificacion(id)
    flash(*result['mensaje'])
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/asignaciones/<int:id_estudiante>', methods=['POST', 'GET'])
def obtener_asignaciones(id_estudiante):
    datos = controller.get_asignaciones_por_estudiante(id_estudiante)
    return jsonify(datos)
