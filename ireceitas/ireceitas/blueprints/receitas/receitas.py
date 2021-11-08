from flask import Blueprint, render_template


bp = Blueprint('receitas', __name__, url_prefix='/receitas', template_folder='templates')


# @bp.route('/')
# def root():
#     return 'Hello from receitas'

@bp.route('/massas')
def massas():
    return render_template("MassasCarrossel.html")

@bp.route('/comidasfit')
def comidasfit():
    return render_template("ComidasFitnessCarrossel.html")

@bp.route('/sobremesas')
def sobremesas():
    return render_template("SobremesasCarrossel.html")

def init_app(app):
    app.register_blueprint(bp)