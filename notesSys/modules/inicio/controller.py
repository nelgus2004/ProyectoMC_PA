from flask import request
from notesSys.database.db import mysql

class indexController:
    def index(self):
        return 'Hello, World!'
