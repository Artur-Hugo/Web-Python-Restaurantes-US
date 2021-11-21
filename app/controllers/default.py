from flask import render_template, request
from flask.helpers import send_file
from app import app, db
from flask_mysqldb import MySQL
from app.models.tables import Pessoa



app.debug = True

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

@app.route('/')
@app.route('/listagem')
def listagem():
    
     #create cursor
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM pessoas")

    pessoas = cur.fetchall()

    
    return render_template('listagem.html',pessoas=pessoas)
    


    
@app.route('/selecao/<int:id>')
def selecao(id=0):
    #create cursor
    cur = mysql.connection.cursor()

    #get article
    result = cur.execute("SELECT * FROM pessoas WHERE id = %s",[id])

    pessoas = cur.fetchone()


    
    return render_template('listagem.html', pessoas=pessoas)

@app.route('/ordenacao/<campo>/<ordem_anterior>')
def ordenacao(campo='id', ordem_anterior=''):
    if campo == 'id':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.id.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.id).all()
    elif campo == 'nome':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.nome.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.nome).all()
    elif campo == 'idade':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.idade.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.idade).all()
    elif campo == 'sexo':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.sexo.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.sexo).all()
    elif campo == 'salario':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.sexo.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.sexo.all())
    else:
        pessoas = Pessoa.query.order_by(Pessoa.id).all()
        
    return render_template('listagem.html', pessoas=pessoas, ordem=campo)

@app.route('/consulta', methods=['POST'])
def consulta():
    consulta = '%'+request.form.get('consulta')+'%'
    campo = request.form.get('campo')

    if campo == 'nome':
        pessoas = Pessoa.query.filter(Pessoa.nome.like(consulta)).all()
    elif campo == 'idade':
        pessoas = Pessoa.query.filter(Pessoa.idade.like(consulta)).all()
    elif campo == 'sexo':
        pessoas = Pessoa.query.filter(Pessoa.sexo.like(consulta)).all()
    elif campo == 'salario':
        pessoas = Pessoa.query.filter(Pessoa.salario.like(consulta)).all()
    else:
        pessoas = Pessoa.query.all()

    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/insercao')
def insercao():
    return render_template('insercao.html')

@app.route('/salvar_insercao', methods=['POST'])

def salvar_insercao():
    form = Pessoa(request.form)
    Nome = form.nome.data
    Idade = form.idade.data
    Sexo = form.sexo.data
    Salario = form.salario.data

    
    

    cur = mysql.connection.cursor()

    #get articles
    cur.execute("INSERT INTO pessoas(nome, idade, sexo, salario) VALUES(%s,%s,%s,%s)",(Nome, Idade, Sexo, Salario))

# commit to DB
    mysql.connection.commit()
    #close connection
    pessoas = cur.fetchone()
    cur.close()


    

    
    return render_template('insercao.html', pessoas=pessoas)

