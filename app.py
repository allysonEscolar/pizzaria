from flask import Flask, render_template, flash, redirect, request, url_for # type: ignore
from utils import db, lm
import os
from flask_migrate import Migrate # type: ignore
from models import *
from controllers.diario import bp_diario


app = Flask(__name__)
app.register_blueprint(bp_diario, url_prefix='/diario')
app.register_blueprint(bp_usuario, url_prefix='/usuario')


# Construção da String de conexão
username = os.getenv('DB.USERNAME')
password = os.getenv('DB.PASSWORD')
host = os.getenv('DB.HOST')
database = os.getenv('DB.DATABASE')

conexao = app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database}'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = conexao

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    print(conexao)
    return render_template('index.html')

@app.route("/cardapio")
def cardapio():
    return render_template('cardapio.html')

@app.route('/avaliacoes')
def avaliacoes():
    dados = [{'cliente': 'Alba', 'nota': 3},
             {'cliente': 'Maria', 'nota': 5},
             {'cliente': 'João', 'nota': 2}
            ]
    return render_template('avaliacoes.html', dados=dados)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form["email"]
    senha = request.form["senha"]
    if (email=="admin@email.com" and senha=="123"):
        return 'Bem vindo admin'
    else:
        flash('E-mail ou senha inválidos', 'danger')
        flash('Tente novamente', 'warning')

        return redirect(url_for('login'))
        #return redirect('/login2')

@app.route('/cadastro_usuarios', methods=['GET', 'POST'])
def cadastro_usuarios():
    if request.method=='GET':
        return render_template('cadastro_usuarios.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        csenha = request.form['csenha']

        if nome == '' or email == '' or senha == '' or senha != csenha:
            if nome == '':
                flash('Campo nome não pode ser vazio', 'danger')
            if email == '':
                flash('Campo email não pode ser vazio', 'danger')
            if senha == '':
                flash('Campo senha não pode ser vazio', 'danger')
            if senha != csenha:
                flash('As senhas não conferem', 'danger')
        else:
            flash('Dados cadastrados com sucesso!', 'success')

        return redirect(url_for('cadastro_usuarios'))

@app.route('/add_diario')
def add_diario():
    d = Diario('Lic001','Desensvolvimento Web')
    db.session.add(d)
    db.session.commit()
    return "Dados Inseridos com Sucesso"

@app.route("/select_diario_all")
def select_diario():
    dados = Diario.query.all()
    for d in dados:
        print('ID: '+ str(d.id)+ ', Disciplina: ' +  d.disciplina +', Titulo: '+d.titulo)
    return 'Dados obtidos com sucesso.'

@app.route("/select_diario/<id>")
def select_diario_id(id):
    dados = Diario.query.get(id)
    
    if(dados):
        print('ID: '+ str(dados.id)+ ', Disciplina: ' +  dados.disciplina +', Titulo: '+dados.titulo)
        return 'Dados obtidos com sucesso.'

    return 'Nenhum dado encontrado com o id: ' + id

@app.route("/update_diario/<id>")
def update_diario(id):
    dados = Diario.query.get(id)
    
    if(dados):
        dados.disciplina = "Seguranca da Informação"
        dados.titulo = "Lic002"
        db.session.add(dados)
        db.session.commit()
        return 'Dados atualizados com Sucesso'
    
    return "Nenhum dado encontrado com o id: " + id

@app.route("/delete_diario/<id>")
def delete_diario(id):
    dados = Diario.query.get(id)
    
    if(dados):
        db.session.delete(dados)
        db.session.commit()
        return 'Dados excluídos com Sucesso'
    
    return "Nenhum dado encontrado com o id: " + id