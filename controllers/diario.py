from flask import render_template, request, redirect, flash, Blueprint, abort, url_for
from jinja2 import TemplateNotFound
from utils import db
from models.diario import Diario
from flask_login import login_required

bp_diario = Blueprint("diario", __name__, template_folder='templates')

@bp_diario.route('/recovery')
@login_required
def recovery():
    dados = Diario.query.all()
 
    # try:
    #     return render_template('diario_recovery.html', dados = dados)
    # except TemplateNotFound:
    #     abort(404)
    return render_template('diario_recovery.html', dados = dados)

@bp_diario.route('/create', methods=['GET', 'POST'])
def create():
    if(request.method == 'GET'):
        return render_template('diario_create.html')
    if(request.method == 'POST'):
        titulo = request.form['titulo']
        disciplina = request.form['disciplina']
        db.session.add(Diario(titulo, disciplina))
        db.session.commit()
        return redirect(url_for('diario.recovery'))

