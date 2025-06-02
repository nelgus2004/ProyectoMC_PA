from flask import Flask
from DigiNote.database import db
from dotenv import load_dotenv
import os

load_dotenv()

def mysql_settings(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql://{os.getenv('MYSQL_USER') or 'adminNotes'}:"
        f"{os.getenv('MYSQL_PASSWORD') or 'admin123.'}@"
        f"{os.getenv('MYSQL_HOST') or '127.0.0.1'}/"
        f"{os.getenv('MYSQL_DB') or 'db_notas'}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    if app.config.get('DEBUG') == True:
        with app.app_context():
            try:
                db.create_all()
                print(" * Base de datos generada correctamente.")
            except Exception as e:
                print(f" * Error al generar la base de datos: {e}")
