from flask import Flask, redirect, url_for, session
from .database.models import Usuario

def init_global_route_app(app: Flask):
    @app.route('/')
    def index():
        return redirect(url_for('inicio.menu'))
    
    @app.context_processor
    def inject_usuario():
        usuario = None
        rol = None
        if 'usuario_id' in session:
            usuario = Usuario.query.get(session['usuario_id'])
            if usuario:
                rol = usuario.Rol
        return dict(usuario=usuario, rol=rol)

    @app.errorhandler(404)
    def not_found(error):
        return "Página no encontrada", 404
