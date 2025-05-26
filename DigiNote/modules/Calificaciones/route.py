from flask import Blueprint, make_response, jsonify
from .controller import MainController


calificacion_bp = Blueprint('calificacion', __name__, template_folder='DigiNote/templates')
controller = MainController()

@calificacion_bp.route('/show')
def show():
    return "<h1>Página enconstrucción</h1>"