from flask import Blueprint, render_template, request, flash,  redirect, url_for
from flask_mail import Message
from flask_login import current_user
from ireceitas.ext.mail import mail

bp = Blueprint('contato', __name__, url_prefix='/contato', template_folder='templates')


# @bp.route('/')
# def root():
#     return render_template('suporte_email.html')

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