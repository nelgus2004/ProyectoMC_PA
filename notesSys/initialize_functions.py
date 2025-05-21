from flask import Flask
from notesSys.modules import all_routes
from notesSys.database.db import mysql, mysql_settings

def initialize_route(app: Flask):
    with app.app_context():
        for modulo, url in all_routes:
            app.register_blueprint(modulo, url_prefix=url)

def initialize_db(app: Flask):
    with app.app_context():
        mysql_settings(app)
