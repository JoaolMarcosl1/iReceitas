from flask import Flask
from flask_mail import Mail

from typing import NoReturn

mail = Mail()

def init_app(app : Flask) -> NoReturn:
    mail.init_app(app)