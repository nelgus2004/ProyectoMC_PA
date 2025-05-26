from flask import Blueprint, make_response, url_for
from ..inicio.route import menu
from .controller import MainController


usuario_bp = Blueprint('auth', __name__, template_folder='DigiNote/templates')
controller = MainController()

@usuario_bp.route('/show')
def show():
    return "<h1>Página en construcción</h1>"

@usuario_bp.route('/show')
def logout():
    return url_for(menu)