from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_login import login_user, logout_user
from ireceitas.ext.database import db
from ireceitas.ext.mail import mail
from ..usuario.entidades import User
from ... import create_app
import os
from werkzeug.utils import secure_filename

bp = Blueprint('autenticacao', __name__, url_prefix='/autenticacao', template_folder='templates')

s = URLSafeTimedSerializer('123456')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        sobre = ""
        if 'foto_perfil' not in request.files:
            flash("Não deu certo inserir essa imagem")
            return redirect(url_for('autenticacao.register'))
        foto = request.files['foto_perfil']

        jatem = User.query.filter_by(email=email).first()

        if jatem is not None:
            flash('Já existe uma conta com esse e-mail. Insira outro e-mail')
            return redirect(url_for('autenticacao.register'))

        else:
            if foto and allowed_file(foto.filename):
                user = User(name, email, pwd, sobre)

                token = s.dumps(email, salt='email-confirm')
                msg = Message('Confirmação de e-mail, iReceitas', sender="receitasprojetoint@gmail.com", recipients=[email])
                link = url_for('autenticacao.confirm_email', token=token, _external=True)
                msg.body = 'Confirme seu e-mail, link: {}'.format(link)
                msg.html = render_template('ativacao_conta.html', link=link)
                mail.send(msg)
                flash('Foi enviado um e-mail de confirmação de conta!')

                db.session.add(user)
                db.session.commit()

                filename =  secure_filename(foto.filename)
                filename = filename.split(".")
                id = user.id
                filename = 'PerfilUser' + str(id) + '.' + filename[1]
                user.profile_img = filename

                app = create_app()
                foto.save(os.path.join(app.config['UPLOAD_PERFIL'], filename))

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('autenticacao.login'))
    return render_template('register.html')


@bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()

        user.isactive = True
        db.session.commit()

    except SignatureExpired:
        flash('Token não existe mais!')
        return redirect(url_for('autenticacao.login'))

    flash('Conta ativada com sucesso!')
    return redirect(url_for('autenticacao.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(pwd):
            flash("Email ou senha inválidos!")
            return redirect(url_for('autenticacao.login'))
        if user.isactive:
            if not user or not user.verify_password(pwd):
                flash("Email ou senha inválidos!")
                return redirect(url_for('autenticacao.login'))
            login_user(user)
            flash('Você foi logado com sucesso :)\n')
            return redirect(url_for('root'))
        else:
            flash("Sua conta não foi ativada")
    return render_template('login.html')

@bp.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("root"))

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root'))

def init_app(app):
    app.register_blueprint(bp)