# route.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import MatriculaController
from datetime import date

matricula_bp = Blueprint('matricula', __name__, template_folder='DigiNote/templates')
controller = MatriculaController()
    
@matricula_bp.route('/')
def show():
    matriculas, asignaciones = controller.show_matricula()
    
    matricula_materias = {}
    for asig in asignaciones:
        idM = asig['idMatricula']
        if idM not in matricula_materias:
            matricula_materias[idM] = []
        matricula_materias[idM].append(asig)
    print(matricula_materias)

    foreign = controller.foreign_records()
    fecha_actual = date.today().isoformat()
    return render_template(
        'matricula.html',
        registros=matriculas,
        materias=matricula_materias,
        fecha_actual = fecha_actual,
        foraneo=foreign,
        active_page='matr',
        r_get=url_for('matricula.get', id='').rstrip('/'),
        r_update=url_for('matricula.update', id='').rstrip('/'),
        campos=['idEstudiante', 'Nivel', 'FechaMatricula', 'PromedioAnual']
    )

@matricula_bp.route('/add_matricula', methods=['POST'])
def add():
    result = controller.add_matricula(request)
    flash(*result)
    return redirect(url_for('matricula.show'))

@matricula_bp.route('/get_matricula/<id>', methods=['GET', 'POST'])
def get(id):
    result = controller.get_matricula_by_id(id)
    return jsonify(result)

@matricula_bp.route('/update_matricula/<id>', methods=['POST'])
def update(id):
    result = controller.update_matricula(id, request)
    flash(*result)
    return redirect(url_for('matricula.show'))

@matricula_bp.route('/delete_matricula/<string:id>', methods=['POST', 'GET'])
def delete(id):
    result = controller.delete_matricula(id)
    flash(*result)
    return redirect(url_for('matricula.show'))
