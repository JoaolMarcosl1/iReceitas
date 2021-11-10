from flask import Blueprint, request, redirect, render_template, flash

from ..usuario.entidades import Receitas
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
            filename =  secure_filename(img.filename)

            app = create_app()
            img.save(os.path.join(app.config['UPLOAD_RECEITAS'], filename))

            receitas = Receitas(filename, titulo, desc, tempo_preparo, rendimento, userID)

            db.session.add(receitas)
            db.session.commit()
        else:
            flash("A extensão deste arquivo não é permitida!")
            return redirect(f'/receitasUsuario/cadastrarReceitas/{id}')


    return render_template("cadastrarReceitas.html" )


def init_app(app):
    app.register_blueprint(bp)