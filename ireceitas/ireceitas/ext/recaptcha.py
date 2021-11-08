from flask import Flask
from flask_recaptcha import ReCaptcha
from typing import NoReturn

recaptcha = ReCaptcha()

def init_app(app : Flask) -> NoReturn:
    recaptcha.init_app(app)