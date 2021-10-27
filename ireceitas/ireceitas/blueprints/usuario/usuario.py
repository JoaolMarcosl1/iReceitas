from flask import Blueprint


bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')


@bp.route('/')
def root():
    return 'Seja bem vindo!'


def init_app(app):
    app.register_blueprint(bp)