from flask import Flask, redirect, url_for 
from DigiNote.config.config import get_config_by_name
from DigiNote.modules import all_routes
from DigiNote.database.db import mysql_settings

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
    
#    print("\nList of registered routes:")
#    for rule in app.url_map.iter_rules():
#        print(f"Endpoint: {rule.endpoint} -> URL: {rule}")
    
    return app
