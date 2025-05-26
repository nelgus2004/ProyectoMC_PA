from flask import Blueprint, make_response, jsonify
from .controller import MainController


curso_bp = Blueprint('curso', __name__, template_folder='DigiNote/templates')
main_controller = MainController()

@curso_bp.route('/show')
def show():
    return "<h1>Página en construcción</h1>"
      