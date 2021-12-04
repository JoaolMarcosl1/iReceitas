from flask_basicauth import BasicAuth
from flask import Flask


from typing import NoReturn

basic_auth = BasicAuth()

def init_app(app : Flask) -> NoReturn:
    basic_auth.init_app(app)