from flask import Blueprint, render_template, flash
from flask_login import current_user

bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')


# @bp.route('/')
# def root():
#     return render_template('edit.html')

@bp.route('/perfil')
def perfil():
    if not current_user.is_authenticated:
        flash("\nSomente quem esta logado pode acessar o seu perfil.")
    else:
        flash(".")
    return render_template("perfil_user.html")

def init_app(app):
    app.register_blueprint(bp)