from flask import Blueprint, make_response, jsonify
from .controller import MainController


matricula_bp = Blueprint('matricula', __name__, template_folder='notesSys/modules/templates')
controller = MainController()
@matricula_bp.route('/', methods=['GET'])
def matricula():
    result=controller.index()
    return make_response(jsonify(data=result))
      