import os
from flask import Blueprint, request, redirect, render_template, flash,  send_from_directory, url_for
from flask_login import login_required
from PIL import Image
from werkzeug.utils import secure_filename
from ..usuario.entidades import Receitas, User, Comentarios
from ...ext.database import db
from ... import create_app

bp = Blueprint('receitasUsuario', __name__, url_prefix='/receitasUsuario', template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/cadastrarReceitas/<int:id>', methods=['GET', 'POST'])
@login_required
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

            app = create_app()
            img.save(os.path.join(app.config['UPLOAD_RECEITAS'], filename))

            imagem = Image.open(os.path.join(app.config['UPLOAD_RECEITAS'], filename))
            imagem.thumbnail((1280,720))
            imagem.save(os.path.join(app.config['UPLOAD_RECEITAS'],filename))

            receitas.img = filename
            db.session.add(receitas)
            db.session.commit()
            return redirect(f'/receitasUsuario/minhasReceitas/{id}')
        else:
            flash("A extensão deste arquivo não é permitida!")
            return redirect(f'/receitasUsuario/cadastrarReceitas/{id}')


    return render_template("cadastrarReceitas.html" )


@bp.get('/minhasReceitas/<int:id>')
@login_required
def minhasReceitas(id):
    usuario = User.query.get(id)
    return render_template('receitasUsuario.html', usuario=usuario)

@bp.get('/receita/<int:id>')
def receita(id):
    receita = Receitas.query.get(id)
    return render_template("receita.html", receita = receita)

@bp.get('/receitaPublica/<int:id>')
@login_required
def receitaPublica(id):
    receita = Receitas.query.get(id)
    return render_template("receitaPublica.html", receita = receita)

@bp.get('/imagemReceitas/<nome>')
@login_required
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_RECEITAS'], nome)

@bp.route("/delete_receita/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_receita(id):
    receita = Receitas.query.get(id)
    app = create_app()
    os.remove(os.path.join(app.config['UPLOAD_RECEITAS'], receita.img))
    db.session.delete(receita)
    db.session.commit()
    return redirect(url_for('usuario.perfil'))

@bp.route("/edit_receita/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_receita(id):
    receita = Receitas.query.get(id)
    user = User.query.get(receita.userID)
    if request.method == 'POST':

        receita.titulo = request.form['titulo']
        receita.tempo_preparo = request.form['tempo_preparo']
        receita.rendimento = request.form['rendimento']
        descricao = request.form['descricao']


        if descricao != '':
            receita.descricao = descricao

        if 'imagemReceitas' in request.files:
            img = request.files['imagemReceitas']

            if img:
                if allowed_file(img.filename):
                    app = create_app()
                    os.remove(os.path.join(app.config['UPLOAD_RECEITAS'], receita.img))
                    filename =  secure_filename(img.filename)
                    filename = filename.split(".")
                    filename = 'User' + str(user.id) + 'Receita' + str(receita.id) + '.' + filename[1]
                    receita.img = filename
                    img.save(os.path.join(app.config['UPLOAD_RECEITAS'], filename))
                    imagem = Image.open(os.path.join(app.config['UPLOAD_RECEITAS'], filename))
                    imagem.thumbnail((1280,720))
                    imagem.save(os.path.join(app.config['UPLOAD_RECEITAS'],filename))
                else:
                    flash("A extensão deste arquivo não é permitida!")
                    return redirect(f'/receitasUsuario/edit_receita/{id}')

        db.session.commit()
        flash("Edição feita com sucesso")
        return redirect(f'/receitasUsuario/minhasReceitas/{user.id}')

    return render_template("editarReceita.html", receita = receita)

#----------comentarios do usuarios nas receitas----------
@bp.post('/addComentario')
@login_required
def addComentario():
    comentario = request.form['comentario']

    publicar_comentario = Comentarios()
    idReceita = request.form['idReceita']
    publicar_comentario.comentario = comentario
    publicar_comentario.receitaID = idReceita
    publicar_comentario.userID = request.form['idUsuario']

    db.session.add(publicar_comentario)
    db.session.commit()
    return redirect(f'/receitasUsuario/receitaPublica/{idReceita}')

@bp.post('/editarComentario')
@login_required
def editarComentario():
    idComentario = request.form['idComentario']
    comentario_editado = request.form['comentario']
    idReceita = request.form['idReceita']
    comentario = Comentarios.query.get(idComentario)

    comentario.comentario = comentario_editado

    db.session.commit()

    return redirect(f'/receitasUsuario/receitaPublica/{idReceita}')

@bp.post('/apagarComentario')
@login_required
def apagarComentario():
    idComentario = request.form['idComentario']
    idReceita = request.form['idReceita']
    comentario = Comentarios.query.get(idComentario)
    db.session.delete(comentario)
    db.session.commit()
    return redirect(f'/receitasUsuario/receitaPublica/{idReceita}')

def init_app(app):
    app.register_blueprint(bp)