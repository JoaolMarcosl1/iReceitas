from flask import Blueprint,  request, redirect, url_for, flash, render_template, abort
from flask_login import current_user
from flask_mail import Message
from flask_admin.contrib.sqla import ModelView
from itsdangerous import  SignatureExpired, URLSafeTimedSerializer
from ireceitas.ext.database import db
from ireceitas.ext.basicauth import basic_auth
from ireceitas.ext.mail import mail
from ireceitas.ext.admin import admin
from ..usuario.entidades import User, Receitas, Comentarios

s = URLSafeTimedSerializer('123456')

bp = Blueprint('usuario_admin', __name__, url_prefix='/usuario_admin', template_folder='templates')


@bp.route('/secret', methods=['GET', 'POST'])
@basic_auth.required
def secret_view():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        sobre = ""

        jatem = User.query.filter_by(email=email).first()
        if jatem is not None:
            flash('Já existe uma conta com esse e-mail. Insira outro e-mail')
            return redirect(url_for('usuario_admin.secret_view'))

        else:
            user = User(name, email, pwd, sobre, isadmin=True)
            token = s.dumps(email, salt='email-confirm-admin')
            msg = Message('Confirmação de e-mail admin, iReceitas', sender="receitasprojetoint@gmail.com", recipients=[email])
            link = url_for('usuario_admin.confirm_email_admin', token=token, _external=True)
            msg.body = 'Confirme seu e-mail, link: {}'.format(link)
            msg.html = render_template('ativacao_conta.html', link=link)
            mail.send(msg)
            db.session.add(user)
            db.session.commit()
            flash('Foi enviado um e-mail de confirmação de conta admin!')
            return redirect(url_for('root'))

    return render_template('secret.html')


@bp.route('/confirm_email_admin/<token>', methods=['GET', 'POST'])
def confirm_email_admin(token):
    try:
        email = s.loads(token, salt='email-confirm-admin', max_age=3600)
        user = User.query.filter_by(email=email).first()

        user.isactive = True
        db.session.commit()

    except SignatureExpired:
        flash('Token não existe mais!')
        return redirect(url_for('autenticacao.login'))

    flash('Conta admin ativada com sucesso!')
    return redirect(url_for('autenticacao.login'))

#Controlador para entrar no /admin
class controller(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return abort(404)
        if current_user.isadmin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
        #return current_user.is_authenticated

    def not_auth(self):
        return "Somente admin pode ter acesso!"

#Admin geral usando bootstrap para template personalizado

admin.add_view(controller(User, db.session))
admin.add_view(ModelView(Comentarios, db.session))
# admin.add_view(ModelView(Receitas, db.session))
# admin.add_view(controller(Comentarios, db.session))


def init_app(app):
    app.register_blueprint(bp)