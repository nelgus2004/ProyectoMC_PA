from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import CalificacionesController

calificacion_bp = Blueprint('calificacion', __name__, template_folder='DigiNote/templates')
controller = CalificacionesController()

@calificacion_bp.route('/')
def show():
    registros = controller.show_calificaciones()
    foreign = controller.foreign_records()
    print(foreign)
    return render_template(
        'calificacion.html',
        registros=registros,
        foraneo=foreign,
        active_page='calif',
        r_add=url_for('calificacion.add'),
        r_get=url_for('calificacion.get_calificacion', id_matricula=0, quimestre=0).rsplit('/', 1)[0],
        r_update=url_for('calificacion.update', id=0).rsplit('/', 1)[0],
        r_delete=url_for('calificacion.delete', id=0).rsplit('/', 1)[0],
        r_asignaciones=url_for('calificacion.obtener_asignaciones', id_estudiante=0).rsplit('/', 1)[0]
    )

@calificacion_bp.route('/add', methods=['POST'])
def add():
    resultado = controller.add_calificacion(request)
    flash(*resultado)
    return redirect(url_for('calificacion.show'))

@calificacion_bp.route('/get/<int:id_matricula>/<int:quimestre>', methods=['GET'])
def get_calificacion(id_matricula, quimestre):
    calificacion = controller.get_calificacion_by_id(id_matricula=id_matricula, quimestre=quimestre)
    if not calificacion:
        return jsonify({})

    return jsonify(calificacion)

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

@calificacion_bp.route('/asignaciones/<int:id_estudiante>', methods=['POST', 'GET'])
def obtener_asignaciones(id_estudiante):
    datos = controller.get_asignaciones_por_estudiante(id_estudiante)
    return jsonify(datos)
