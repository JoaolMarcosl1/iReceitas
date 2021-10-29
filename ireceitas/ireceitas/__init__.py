from flask import Flask, render_template
from ireceitas.ext import configuration
from .views import root


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    app.add_url_rule('/', view_func=root)

    @app.errorhandler(404)#Caso usuário acesse uma pagina que não existe
    def not_found(e):
        return render_template("404.html")

    return app