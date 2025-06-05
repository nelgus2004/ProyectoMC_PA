from flask import Flask, redirect, url_for 
from .config.config import get_config_by_name
from .modules import all_routes
from .database.db import mysql_settings
from .modules.Usuario.controller import crear_superadmin

def create_app(config=None) -> Flask:
    app = Flask(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))

    # Inizializar extensiones de la base de datos mysql
    mysql_settings(app)
    
    # Registrar blueprints (rutas    
    for modulo, url in all_routes:
            app.register_blueprint(modulo, url_prefix=url)
    
    from . import app as app_module
    app_module.init_global_route_app(app)
    
    # Crear usuario superAdmin inicial
    with app.app_context():
        from .modules.Usuario.controller import crear_superadmin
        crear_superadmin()
    
    print("\nLista de rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f" * Endpoint: {rule.endpoint} -> URL: {rule}")
    
    return app
