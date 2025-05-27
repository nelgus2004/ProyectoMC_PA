from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from .controller import CalificacionesController

calificacion_bp = Blueprint('calificacion', __name__, template_folder='DigiNote/templates')
controller = CalificacionesController()

@calificacion_bp.route('/')
def show():
    result = ''
    foreign = ''
    return render_template(
        'calificacion.html'
    )
    
@calificacion_bp.route('/add_calificacion', methods=['POST'])
def add():
    return "<p>text</p>"