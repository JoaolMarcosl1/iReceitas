import os
from flask import Blueprint, render_template, flash, request, url_for, redirect, send_from_directory
from flask_login import current_user, login_required
from PIL import Image
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from .entidades import User
from ...ext.database import db
from ... import create_app


bp = Blueprint('usuario', __name__, url_prefix='/usuario', template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/perfil')
@login_required
def perfil():
    if not current_user.is_authenticated:
        flash("\nSomente quem esta logado pode acessar o seu perfil.")
    else:
        flash(".")
    return render_template("perfil_user.html")

@bp.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':

        user.name = request.form['name']
        user.sobre = request.form['sobre']
        foto = request.files['foto_perfil']
        resetar_imagem = "nao"
        if 'resetar_imagem' in request.form:
            resetar_imagem = request.form['resetar_imagem']
        try:
            db.session.commit()

            if foto and allowed_file(foto.filename):
                app = create_app()
                if user.profile_img != 'default_perfil.png':
                    os.remove(os.path.join(app.config['UPLOAD_PERFIL'], user.profile_img))
                filename =  secure_filename(foto.filename)
                filename = filename.split(".")
                id = user.id
                filename = 'PerfilUser' + str(id) + '.' + filename[1]
                foto.save(os.path.join(app.config['UPLOAD_PERFIL'], filename))

                imagem = Image.open(os.path.join(app.config['UPLOAD_PERFIL'], filename))
                imagem.thumbnail((300,300))
                imagem.save(os.path.join(app.config['UPLOAD_PERFIL'],filename))
                user.profile_img = filename
                db.session.commit()

            if resetar_imagem == "sim":
                if user.profile_img != 'default_perfil.png':
                    app = create_app()
                    os.remove(os.path.join(app.config['UPLOAD_PERFIL'], user.profile_img))
                    user.profile_img = 'default_perfil.png'
                    db.session.add(user)
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

@bp.route('/perfil_publico/<int:id>', methods=['GET', 'POST'])
@login_required
def perfil_publico(id):
    user = User.query.get(id)

    return render_template("perfil_publico.html", usuario = user)

@bp.route('/buscar_usuario', methods=['GET', 'POST'])
@login_required
def buscar_usuario():
    usuarios = User.query.all()
    nomes_usuarios = [usuario.name for usuario in usuarios]
    id_usuarios = [usuario.id for usuario in usuarios]
    fotos_usuarios = [usuario.profile_img for usuario in usuarios]

    if request.method == 'POST':
        nome = request.form["nome"]
        search = "%{}%".format(nome)
        user = User.query.filter(User.name.like(search)).all()

        return render_template("listaDeUsuarios.html", usuarios = user)
    return render_template("buscar_usuario.html", nomes_usuarios = nomes_usuarios, id_usuarios = id_usuarios, fotos_usuarios = fotos_usuarios)

@bp.get('/imagem/<nome>')
@login_required
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_PERFIL'], nome)



def init_app(app):
    app.register_blueprint(bp)