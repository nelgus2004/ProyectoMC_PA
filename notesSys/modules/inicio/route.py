from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response, jsonify
from .controller import indexController


index_bp = Blueprint('inicio', __name__, template_folder='../notesSys/templates')
controller  = indexController()

@index_bp.route('/inicio/')
def menu():
    #result=controller.index()
    return render_template('inicio.html')


#@index_bp.route('/loging')
#def index():
#    return redirect(url_for('inicio.login'))