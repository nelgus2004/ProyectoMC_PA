from flask import Flask, redirect, url_for 
from notesSys.config.config import get_config_by_name
from notesSys.initialize_functions import initialize_route, initialize_db

def create_app(config=None) -> Flask:
    app = Flask(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))

    # Inizializar extensiones de la base de datos mysql
    initialize_db(app)

    # Registrar blueprints (rutas
    initialize_route(app)
    
    @app.route('/')
    def index():
        return redirect(url_for('inicio.menu'))
    
    #print("\nList of registered routes:")
    #for rule in app.url_map.iter_rules():
    #    print(f"Endpoint: {rule.endpoint} -> URL: {rule}")
    
    return app
