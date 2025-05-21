from flask import Blueprint, make_response, jsonify
from .controller import MainController


estudiante_bp = Blueprint('estudiante', __name__, template_folder='notesSys/modules/templates')
controller = MainController()

@estudiante_bp.route('/', methods=['GET'])
def estudiante():
    result=controller.index()
    return make_response(jsonify(data=result))
      