from flask import render_template, flash
from flask_login import current_user

def root():
    if not current_user.is_authenticated:
        flash("\nVocê não esta logado.")
    else:
        flash(f"\n\nOlá {current_user.name}, seja bem vindo(a).")
    return render_template('index.html')

