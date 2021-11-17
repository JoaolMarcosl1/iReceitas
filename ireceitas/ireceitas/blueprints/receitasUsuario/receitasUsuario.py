from flask import Blueprint, request, redirect, render_template, flash,  send_from_directory, url_for
from flask_login import login_required
from ..usuario.entidades import Receitas, User
from ...ext.database import db
from ... import create_app
import os
from werkzeug.utils import secure_filename
bp = Blueprint('receitasUsuario', __name__, url_prefix='/receitasUsuario', template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/cadastrarReceitas/<int:id>', methods=['GET', 'POST'])
def cadastrarReceitas(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        desc = request.form['descricao']
        tempo_preparo = request.form['tempo_preparo']
        rendimento = request.form['rendimento']
        img = request.files['imagemReceitas']
        userID = id

        if img and allowed_file(img.filename):

            receitas = Receitas(titulo, desc, tempo_preparo, rendimento, userID)
            db.session.add(receitas)
            db.session.commit()

            filename =  secure_filename(img.filename)
            filename = filename.split(".")
            idReceitas = receitas.id

            filename = 'User' + str(id) + 'Receita' + str(idReceitas) + '.' + filename[1]
            receitas.img = filename

            app = create_app()
            img.save(os.path.join(app.config['UPLOAD_RECEITAS'], filename))

            db.session.add(receitas)
            db.session.commit()
        else:
            flash("A extensão deste arquivo não é permitida!")
            return redirect(f'/receitasUsuario/cadastrarReceitas/{id}')


    return render_template("cadastrarReceitas.html" )


@bp.get('/minhasReceitas/<int:id>')
def minhasReceitas(id):
    usuario = User.query.get(id)
    return render_template('receitasUsuario.html', usuario=usuario)

@bp.get('/receita/<int:id>')
def receita(id):
    receita = Receitas.query.get(id)
    return render_template("receita.html", receita = receita)

@bp.get('/imagemReceitas/<nome>')
@login_required
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_RECEITAS'], nome)

@bp.route("/delete_receita/<int:id>", methods=['GET', 'POST'])
def delete_receita(id):
    receita = Receitas.query.get(id)
    app = create_app()
    os.remove(os.path.join(app.config['UPLOAD_RECEITAS'], receita.img))
    db.session.delete(receita)
    db.session.commit()

    return redirect(url_for('usuario.perfil'))

def init_app(app):
    app.register_blueprint(bp)