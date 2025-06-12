from flask import Flask, redirect, url_for, session, request, jsonify, get_flashed_messages
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

    @app.route('/get_flashed_messages', methods=['GET'])
    def get_flashed_messages_api():
        # Guarda los mensajes en sesión antes de limpiarlos
        saved_messages = session.get('pending_flash_messages', [])
        new_messages = get_flashed_messages(with_categories=True)
        all_messages = saved_messages + new_messages
        
        # Guarda los mensajes no consumidos para próximas peticiones
        session['pending_flash_messages'] = all_messages
        return jsonify(all_messages)

    @app.route('/clear_flash_messages', methods=['POST'])
    def clear_flash_messages():
        # Limpia los mensajes cuando el cliente confirma recepción
        session.pop('pending_flash_messages', None)
        return jsonify({'status': 'success'})
        
    

    @app.errorhandler(404)
    def not_found(error):
        return "Página no encontrada", 404
    
    @app.errorhandler(500)
    def not_found(error):
        return "Error de servidor", 500
