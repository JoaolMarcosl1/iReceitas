from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import current_user
from ...ext.database import db
from .entidades import User
from sqlalchemy.exc import IntegrityError

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

@bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':

        user.name = request.form['name']
        user.email = request.form['email']
        user.sobre = request.form['sobre']

        try:
            db.session.commit()
            flash("Alteração feita com sucesso!")
            return redirect(url_for('root'))

        except IntegrityError:
            flash("Opa! Esse e-mail ja esta sendo utilizado.")
            return redirect(url_for('root'))

            #return "E-mail existe"
            #db.session.commit()
           # return "Deu certo, você mudou o e-mail"
       # db.session.commit()
       # return redirect(url_for('home'))
        #jatem = User.query.filter_by(email=user.email).first()
       # if jatem is not None:
           # return "E-mail existe"
      #  else:
    return render_template("edit.html", user=user)

def init_app(app):
    app.register_blueprint(bp)