from flask import Flask, render_template, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/avaliacoes')
def avaliacoes():
    arquivo = open("static/dados.json")
    dados = json.load(arquivo)
    return render_template('avaliacoes.html', dados=dados)    

if __name__ == '__main__':
    app.run()
