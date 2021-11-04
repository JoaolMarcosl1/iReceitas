from flask import Blueprint, render_template, flash, request, url_for, redirect, send_from_directory
from flask_login import current_user, login_required
from ...ext.database import db
from .entidades import User
from sqlalchemy.exc import IntegrityError
from ... import create_app
import os
from werkzeug.utils import secure_filename

bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            if 'foto_perfil' not in request.files:
                flash("Não deu certo inserir essa imagem")
                return redirect(url_for('usuario.edit'))

            foto = request.files['foto_perfil']
            filename =  secure_filename(foto.filename)
            filename = filename.split(".")
            id = user.id
            filename = 'PerfilUser' + str(id) + '.' + filename[1]
            user.profile_img = filename

            app = create_app()
            foto.save(os.path.join(app.config['UPLOAD_PERFIL'], filename))
            db.session.commit()
            flash("Alteração feita com sucesso!")
            return redirect(url_for('root'))

        except IntegrityError:
            flash("Opa! Esse e-mail ja esta sendo utilizado.")
            return redirect(url_for('usuario.perfil'))

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

@bp.get('/imagem/<nome>')
@login_required
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_PERFIL'], nome)

def init_app(app):
    app.register_blueprint(bp)