from flask_admin import Admin
from flask import Flask

from typing import NoReturn

admin = Admin(template_mode='bootstrap3')

def init_app(app : Flask) -> NoReturn:
    admin.init_app(app)