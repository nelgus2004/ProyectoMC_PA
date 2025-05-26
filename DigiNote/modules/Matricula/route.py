from flask import Blueprint, make_response, jsonify
from .controller import MainController


matricula_bp = Blueprint('matricula', __name__, template_folder='DigiNote/templates')
controller = MainController()

@matricula_bp.route('/show')
def show():
    return "<h1>Página en construcción</h1>"
      