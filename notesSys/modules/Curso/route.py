from flask import Blueprint, make_response, jsonify
from .controller import MainController


curso_bp = Blueprint('curso', __name__, template_folder='notesSys/modules/templates')
main_controller = MainController()

@curso_bp.route('/', methods=['GET'])
def curso():
    result=main_controller.index()
    return make_response(jsonify(data=result))
      