from flask import Blueprint, render_template, request, flash,  redirect, url_for, abort
from flask_mail import Message
from flask_login import current_user
from ireceitas.ext.mail import mail

bp = Blueprint('contato', __name__, url_prefix='/contato', template_folder='templates')


# @bp.route('/')
# def root():
#     return render_template('suporte_email.html')


@bp.route('/report', methods=['GET', 'POST'])
def report():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            motivo = request.form.get('motivo')
            msg = Message(subject=f"Report do usuário - [{nome}]", sender="joaobastos716@gmail.com", recipients=["receitasprojetoint@gmail.com"])
            msg.body = f"{motivo}"
            msg.html = render_template('report_email.html', motivo=motivo, nome=nome, email=email)
            mail.send(msg)
            flash("Seu report foi enviado com sucesso! Aguarde a staff para tomar as devidas providências")
            return redirect(url_for('root'))
    else:
        return abort(404)
    return render_template("report.html")


@bp.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        tittle = request.form.get('tittle')
        message = request.form.get('message')


        #message = message+f"\nReperquilson se garante mais que o {current_user.name}"

        msg = Message(subject=f"Suporte para {current_user.name} | {tittle}",
                      sender="joaobastos716@gmail.com", recipients=["receitasprojetoint@gmail.com"])

        msg.body = f"{message}"
        msg.html = render_template('suporte_email.html', message=message)
        mail.send(msg)
        flash("Sua mensagem foi enviada com sucesso!")


        #msg = Message("Olá, Estou precisando da ajuda de vocês.", sender="joaobastos716@gmail.com", recipients=["receitasprojetoint@gmail.com"])
        #msg.body = "Enviando uma duvida, testando"
        #mail.send(msg)
        return redirect(url_for('root'))


    return render_template("contato.html")


def init_app(app):
    app.register_blueprint(bp)