from flask import Blueprint, render_template, session
from .controller import indexController

index_bp = Blueprint('inicio', __name__, template_folder='DigiNote/templates')
controller  = indexController()

@index_bp.route('/inicio/')
def menu():
    return render_template('inicio.html', active_page='inicio')

#@index_bp.route('/logout')
#def logout():
#    return redirect(url_for('inicio.login'))