from flask import request
from DigiNote.database.db import mysql

class indexController:
    def index(self):
        return 'Hello, World!'
