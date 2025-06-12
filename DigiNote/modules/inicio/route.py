from flask import Blueprint, render_template, session, redirect, url_for
from .controller import indexController

index_bp = Blueprint('inicio', __name__, template_folder='DigiNote/templates')
controller  = indexController()

@index_bp.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('inicio.menu'))

@index_bp.route('/inicio/')
def menu():
    return render_template('inicio.html', active_page='inicio')

