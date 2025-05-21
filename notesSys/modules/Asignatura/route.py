from flask import Blueprint, make_response, jsonify
from .controller import MainController


asignatura_bp = Blueprint('asignatura', __name__, template_folder='notesSys/modules/templates')
main_controller = MainController()
@asignatura_bp.route('/', methods=['GET'])
def asignatura():
    result=main_controller.index()
    return make_response(jsonify(data=result))
      
      
      