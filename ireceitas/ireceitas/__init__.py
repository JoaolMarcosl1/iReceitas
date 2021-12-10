from flask import Flask, render_template
from sqlalchemy.sql import func
from ireceitas.ext import configuration
from .views import root
from .blueprints.usuario.entidades import Avaliacao

def formatar_tempo(tempo):
    hora = int(tempo[0:2])
    minutos = int(tempo[3:6])
    if hora != 0 and minutos == 0 :
        return f'Até {hora}h'
    if minutos != 0 and hora == 0:
        return f'Até {minutos}m'
    return f'Até {hora}h e {minutos}m'


def avaliacao(id, idReceita):
    ava = Avaliacao.query.filter_by(userID=id, receitaID=idReceita).first()
    if ava is None:
        return True
    else:
        return False


def classificacao(idReceita):
    nota = Avaliacao.query.with_entities(func.avg(Avaliacao.nota).label('avg')).filter(Avaliacao.receitaID==idReceita).scalar()
    if nota is None:
        return 'Sem avaliações'
    if nota == int(nota):
        return int(nota)

    return round(nota,1)

def nota_usuario(idUser, idReceita):
    avaliacao = Avaliacao.query.filter_by(userID=idUser, receitaID=idReceita).first()
    if avaliacao is None:
        return False
    nota = avaliacao.nota
    return nota

def quantidade_avalicoes(idReceita):
    qtd_av = Avaliacao.query.with_entities(func.count(Avaliacao.nota)).filter(Avaliacao.receitaID==idReceita).scalar()
    if qtd_av == 0:
        return False
    return qtd_av

def primeiro(ingredientes):
    i = ingredientes[0].id
    return i


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    app.add_url_rule('/', view_func=root)

    app.jinja_env.filters['formatar_tempo'] = formatar_tempo
    app.jinja_env.filters['avaliacao'] = avaliacao
    app.jinja_env.filters['classificacao'] = classificacao
    app.jinja_env.filters['nota_usuario'] = nota_usuario
    app.jinja_env.filters['quantidade_avalicoes'] = quantidade_avalicoes
    app.jinja_env.filters['primeiro'] = primeiro

    @app.errorhandler(404)#Caso usuário acesse uma pagina que não existe
    def not_found(e):
        return render_template("404.html")

    return app