from flask import Blueprint, render_template, Flask


bp = Blueprint('erro', __name__, url_prefix='/erro', template_folder='templates')


@bp.errorhandler(404)#Caso usuário acesse uma pagina que não existe
def not_found(e):
  return render_template("404.html")


def init_app(app):
    app.register_blueprint(bp)