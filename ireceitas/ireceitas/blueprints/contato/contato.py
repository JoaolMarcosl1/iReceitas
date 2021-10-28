from flask import Blueprint, render_template


bp = Blueprint('contato', __name__, url_prefix='/contato', template_folder='templates')


@bp.route('/')
def root():
    return render_template('suporte_email.html')


def init_app(app):
    app.register_blueprint(bp)