from flask import render_template, request, redirect, flash, Blueprint, abort
from jinja2 import TemplateNotFound
from models.database import db
from models.diario import Diario

bp_diario = Blueprint("diario", __name__, template_folder='templates')

@bp_diario.route('/recovery')
def recovery():
    try:
        return render_template('diario_recovery.html')
    except TemplateNotFound:
        abort(404)