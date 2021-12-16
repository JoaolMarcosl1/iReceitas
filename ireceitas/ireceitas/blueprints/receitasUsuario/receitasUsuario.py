import os
from flask import Blueprint, request, redirect, render_template, flash,  send_from_directory, url_for
from flask_login import login_required
from PIL import Image
from datetime import datetime, timezone, timedelta
from werkzeug.utils import secure_filename
from ..usuario.entidades import Receitas, User, Comentarios, Avaliacao, Ingrediente, Etapa, Topico
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

        #  if 'cafe_da_manha' in request.form:


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

            #------------- Para adicionar igredientes em uma receita -----------------

            for ingr in  [x for x in request.form if 'ingrediente' in x]:
                instancia_igrediente = Ingrediente()
                instancia_igrediente.receitaID = idReceitas
                ingrediente = request.form[ingr]
                instancia_igrediente.nome = ingrediente
                db.session.add(instancia_igrediente)
                db.session.commit()

            #------------- Para adicionar etapas em uma receita -----------------

            for etapa in  [x for x in request.form if 'etapa' in x]:
                instancia_etapa = Etapa()
                instancia_etapa.receitaID = idReceitas
                ETAPA = request.form[etapa]
                instancia_etapa.descricao = ETAPA
                db.session.add(instancia_etapa)
                db.session.commit()


            instancia_topico = Topico()
            instancia_topico.receitaID = idReceitas
            instancia_topico.nome = request.form['topico']
            db.session.add(instancia_topico)
            db.session.commit()





            return redirect('/usuario/perfil')
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
@login_required
def receitaPublica(id):
    receita = Receitas.query.get(id)
    return render_template("receita.html", receita = receita)

# @bp.get('/receita/<int:id>')
# @login_required
# def receitaPublica(id):
#     receita = Receitas.query.get(id)
#     return render_template("receitaPublica.html", receita = receita)

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

        #------------- Para editar igredientes em uma receita -----------------

        for ingr in  [x for x in request.form if 'ingrediente' in x]:
            instancia_igrediente = Ingrediente()
            instancia_igrediente.receitaID = id
            ingrediente = request.form[ingr]
            instancia_igrediente.nome = ingrediente
            db.session.add(instancia_igrediente)
            db.session.commit()

        for IngrAtual in  [x for x in request.form if 'IngrAtual' in x]:
            idIngrediente = IngrAtual.split("l")[1]
            ingrediente = Ingrediente.query.get(idIngrediente)
            ingrediente.nome = request.form[IngrAtual]
            db.session.commit()


        # ----------------------Para editar uma etapa------------------------
        for etapaAtual in  [x for x in request.form if 'EtAtual' in x]:
            idEtapa = etapaAtual.split("l")[1]
            etapa = Etapa.query.get(idEtapa)
            etapa.descricao = request.form[etapaAtual]
            db.session.commit()

        # #------------- Para adicionar etapas em uma receita -----------------
        for etapa in  [x for x in request.form if 'ETAPA' in x]:
            instancia_etapa = Etapa()
            instancia_etapa.receitaID = id
            ETAPA = request.form[etapa]
            instancia_etapa.descricao = ETAPA
            db.session.add(instancia_etapa)
            db.session.commit()

        #------------- Para editar um Topico em uma receita -----------------

        idTopico = [id for id in receita.topico]

        if len(idTopico) != 0:
            topico = Topico.query.get(idTopico[0].id)
            topico.nome = request.form['topico']
            db.session.commit()




        flash("Edição feita com sucesso")
        return redirect(f'/receitasUsuario/receita/{id}')

    return render_template("editarReceita.html", receita = receita)

# ------------PARA APAGAR INGREDIENTE----------------
@bp.post('/apagarIngrediente')
@login_required
def apagarIngrediente():
    idIngrediente = request.form['idIngrediente']
    idReceita = request.form['idReceita']
    ingrediente = Ingrediente.query.get(idIngrediente)
    db.session.delete(ingrediente)
    db.session.commit()
    return redirect(f'/receitasUsuario/edit_receita/{idReceita}')

# ------------PARA APAGAR UMA ETAPA---------
@bp.post('/apagarEtapa')
@login_required
def apagarEtapa():
    idEtapa = request.form['idEtapa']
    idReceita = request.form['idReceita']
    etapa = Etapa.query.get(idEtapa)
    db.session.delete(etapa)
    db.session.commit()
    return redirect(f'/receitasUsuario/edit_receita/{idReceita}')


#----------comentarios do usuarios nas receitas----------
@bp.post('/addComentario')
@login_required
def addComentario():

    publicar_comentario = Comentarios()

    data_atual = datetime.now()
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data = data_atual.astimezone(fuso_horario)
    data = data.strftime('%d/%m/%Y %H:%M')

    comentario = request.form['comentario']
    idReceita = request.form['idReceita']
    publicar_comentario.comentario = comentario
    publicar_comentario.receitaID = idReceita
    publicar_comentario.data_hora = data
    publicar_comentario.userID = request.form['idUsuario']

    db.session.add(publicar_comentario)
    db.session.commit()
    return redirect(f'/receitasUsuario/receita/{idReceita}')

@bp.post('/editarComentario')
@login_required
def editarComentario():

    data_atual = datetime.now()
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data = data_atual.astimezone(fuso_horario)
    data = data.strftime('%d/%m/%Y %H:%M')

    idComentario = request.form['idComentario']
    comentario_editado = request.form['comentario']
    idReceita = request.form['idReceita']
    comentario = Comentarios.query.get(idComentario)

    comentario.comentario = comentario_editado
    comentario.data_hora = data
    db.session.commit()

    return redirect(f'/receitasUsuario/receita/{idReceita}')

@bp.post('/apagarComentario')
@login_required
def apagarComentario():
    idComentario = request.form['idComentario']
    idReceita = request.form['idReceita']
    comentario = Comentarios.query.get(idComentario)
    db.session.delete(comentario)
    db.session.commit()
    return redirect(f'/receitasUsuario/receita/{idReceita}')

@bp.post('/desativar_ativar_Comentario')
@login_required
def desativar_ativar_Comentario():
    idReceita = request.form['idReceita']
    ativar = request.form['ativar']
    receita = Receitas.query.get(idReceita)
    receita.comentario_ativado = ativar
    db.session.commit()
    return redirect(f'/receitasUsuario/receita/{idReceita}')

#--------------Buscar receita---------------
@bp.post("/buscarReceita")
@login_required
def buscarReceita():
    titulo = request.form["titulo"]
    search = "%{}%".format(titulo)
    receita = Receitas.query.filter(Receitas.titulo.like(search)).all()
    if len(receita) == 0:
        flash("Receita não encontrada")
        return render_template("listaDeReceitas.html", receitas = receita)
    return render_template("listaDeReceitas.html", receitas = receita)

# -----------------BUSCAR RECEITA POR TOPICO------------
@bp.get("/buscarTopico/<Nometopico>")
@login_required
def buscarTopico(Nometopico):
    # Nometopico = request.form['topico']
    topico = Topico.query.filter_by(nome=Nometopico).all()
    receita =[]
    for t in topico:
      r = Receitas.query.get(t.receitaID)
      receita.append(r)

    if len(topico) == 0:
        flash("Tópico vazio")
        return render_template("listaDeReceitas.html", receitas = receita)
    return render_template("listaDeReceitas.html", receitas = receita)


# -----------------Avaliação receita---------------
@bp.post("/avaliarReceita")
@login_required
def avaliarReceita():
    avaliacao = Avaliacao()
    nota = request.form["nota"]
    idUsuario = request.form['idUsuario']
    idReceita = request.form['idReceita']

    avaliacao.userID = idUsuario
    avaliacao.receitaID = idReceita
    avaliacao.nota = nota

    db.session.add(avaliacao)
    db.session.commit()
    return redirect(f'/receitasUsuario/receita/{idReceita}')

@bp.post("/iditarAvalicao")
@login_required
def iditarAvalicao():

   nota = request.form["nota"]
   idUsuario = request.form['idUsuario']
   idReceita = request.form['idReceita']

   avaliacao = Avaliacao.query.filter_by(userID=idUsuario, receitaID=idReceita).first()

   avaliacao.nota = nota

   db.session.commit()
   return redirect(f'/receitasUsuario/receita/{idReceita}')

@bp.post("/apagarAvaliacao")
@login_required
def apagarAvaliacao():
   idUsuario = request.form['idUsuario']
   idReceita = request.form['idReceita']

   avaliacao = Avaliacao.query.filter_by(userID=idUsuario, receitaID=idReceita).first()

   db.session.delete(avaliacao)
   db.session.commit()
   return redirect(f'/receitasUsuario/receita/{idReceita}')


def init_app(app):
    app.register_blueprint(bp)