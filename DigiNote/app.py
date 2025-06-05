from flask import Flask, redirect, url_for, session, request
from .database.models import Usuario

def init_global_route_app(app: Flask):
    @app.context_processor
    def inject_usuario():
        usuario = None
        if 'usuario_id' in session:
            usuario = Usuario.query.get(session['usuario_id'])
        return dict(usuario=usuario)
    
    @app.before_request
    def validar_sesion():
        rutas_permitidas = ['auth.login', 'auth.login_autenticar', 'auth.register_external', 'auth.logout', 'auth.add_usuario' ,'static']

        if request.endpoint is None or (request.endpoint not in rutas_permitidas and 'usuario_id' not in session):
            return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def not_found(error):
        return "Página no encontrada", 404
    
    @app.errorhandler(500)
    def not_found(error):
        return "Error de servidor", 500
