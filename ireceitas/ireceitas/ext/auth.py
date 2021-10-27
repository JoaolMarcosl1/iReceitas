from flask import Flask
from flask_login import LoginManager


from typing import NoReturn

login_manager = LoginManager()

def init_app(app : Flask) -> NoReturn:
    login_manager.init_app(app)