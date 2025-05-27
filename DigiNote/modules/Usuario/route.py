from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import MainController
from ..inicio.route import menu

usuario_bp = Blueprint('auth', __name__, template_folder='DigiNote/templates')
controller = MainController()

@usuario_bp.route('/')
def show():
    result = ''
    foreign = ''
    return render_template(
        'usuario.html'
    )
    
@usuario_bp.route('/salir')
def logout():
    return url_for(menu)

@usuario_bp.route('/add_usuario', methods=['POST'])
def add():
    return "<p>text</p>"