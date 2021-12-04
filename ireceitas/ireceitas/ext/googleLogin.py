from flask import Flask
from authlib.integrations.flask_client import OAuth

from typing import NoReturn

oauth = OAuth()


def init_app(app : Flask) -> NoReturn:
   oauth.init_app(app)
   oauth.register(
    name = 'google',
    client_id = app.config['OAUTH_GOOGLE_CLIENT_ID'],
    client_secret = app.config['OAUTH_GOOGLE_CLIENT_SECRET'],
    access_token_url = app.config['OAUTH_GOOGLE_ACCESS_TOKEN_URL'],
    access_token_params = None,
    authorize_url = app.config['OAUTH_GOOGLE_AUTHORIZE_URL'],
    authorize_params = None,
    api_base_url = app.config['OAUTH_GOOGLE_API_BASE_URL'],
    client_kwargs = {'scope': 'openid profile email'},
    )