from flask import Blueprint, render_template


bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')


@bp.route('/')
def root():
    return render_template('edit.html')


def init_app(app):
    app.register_blueprint(bp)