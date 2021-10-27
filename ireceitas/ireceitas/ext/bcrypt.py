from flask import Flask
from flask_bcrypt import Bcrypt

from typing import NoReturn

bcrypt = Bcrypt()

def init_app(app : Flask) -> NoReturn:
    bcrypt.init_app(app)