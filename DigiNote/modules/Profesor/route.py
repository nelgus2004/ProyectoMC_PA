from flask import Blueprint, make_response, jsonify
from .controller import MainController


profesor_bp = Blueprint('profesor', __name__, template_folder='notesSys/modules/templates')
controller = MainController()

@profesor_bp.route('/', methods=['GET'])
def profesor():
    result=controller.index()
    return make_response(jsonify(data=result))
      