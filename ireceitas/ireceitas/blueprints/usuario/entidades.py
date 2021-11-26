from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash #senha hash
from ...ext.database import db
from ...ext.auth import login_manager

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin): #usuarios
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(2048), nullable=False)
    sobre = db.Column(db.String(100), nullable=False)
    isactive = db.Column(db.Boolean, default=False)
    profile_img = db.Column(db.String(100), default="default_perfil.png")
    receitas = db.relationship('Receitas', backref='user', lazy=True, cascade="all, delete")
    comentario = db.relationship('Comentarios', backref='user', lazy=True, cascade="all, delete")

    def __init__(self, name, email, password, sobre):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.sobre = sobre

    def setPassword(self, senhanova):
        self.password = generate_password_hash(senhanova)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __str__(self):
        return f'Usuário {self.name} tem o e-mail {self.email}'

class Receitas(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text(), nullable=False)
    tempo_preparo = db.Column(db.String(50), nullable=False)
    rendimento = db.Column(db.String(50), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img = db.Column(db.String(100))
    comentario_ativado = db.Column(db.String(10), default="sim")
    comentario = db.relationship('Comentarios', backref='receitas', lazy=True, cascade="all, delete")

    def __init__(self, titulo, desc, tempo_preparo, rendimento, userID):
        self.titulo = titulo
        self.descricao = desc
        self.tempo_preparo = tempo_preparo
        self.rendimento = rendimento
        self.userID = userID

class Comentarios(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comentario = db.Column(db.Text())
    data_hora = db.Column(db.String(20))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receitaID = db.Column(db.Integer, db.ForeignKey('receitas.id'), nullable=False)
