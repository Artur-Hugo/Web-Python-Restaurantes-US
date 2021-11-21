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