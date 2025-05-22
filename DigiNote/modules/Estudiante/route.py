from flask import Blueprint, render_template, request, make_response, jsonify
from .controller import MainController

estudiante_bp = Blueprint('estudiante', __name__, template_folder='notesSys/modules/templates')
controller = MainController()

#@estudiante_bp.route('/', methods=['GET'])
#def estudiante():
#    result=controller.index()
#    return make_response(jsonify(data=result))
      
@estudiante_bp.route('/')
def show():
    result = controller.show_estudiante()
    return render_template('estudiante.html', registros=result)

@estudiante_bp.route('/add_estudiante', methods=['POST'])
def add():
    if request.method== 'POST':
        result = controller.add_estudiante(request)
        print(result)
    return render_template('estudiante.html')