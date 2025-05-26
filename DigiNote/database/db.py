from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
mysql = MySQL()

def mysql_settings(app: Flask):
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER') or 'adminNotes'
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') or 'admin123.'
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') or '127.0.0.1'
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') or 'db_notas'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql.init_app(app)
    
    if app.config.get('DEBUG') == True:
        sql_path = os.path.join(os.path.dirname(__file__), 'db_notas.sql')
        with app.app_context():
            try:
                cur = mysql.connection.cursor()
                with open(sql_path, 'r', encoding='utf-8') as sql_file:
                    sql_commands = sql_file.read()
                    for command in sql_commands.split(';'):
                        if command.strip() and not command.startswith('--'):
                            cur.execute(command)
                mysql.connection.commit()
                print("* Base de datos generada correctamente.")
                cur.close()
            except Exception as e:
                print(f"* Error al generar la base de datos: {e}")
