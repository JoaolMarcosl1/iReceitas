from flask import Flask
from flask_login import loginManager

from typing import NoReturn

login_manager = loginManager()

def init_app(app : Flask) -> NoReturn:
    login_manager.init_app(app)