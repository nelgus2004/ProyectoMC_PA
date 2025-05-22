from flask import Blueprint, make_response, jsonify
from .controller import MainController


calificacion_bp = Blueprint('calificacion', __name__, template_folder='notesSys/modules/templates')
controller = MainController()
@calificacion_bp.route('/', methods=['GET'])
def calificacion():
    result=controller.index()
    return make_response(jsonify(data=result))
      