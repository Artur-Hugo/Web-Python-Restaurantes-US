from flask import render_template, request
from flask.helpers import send_file
from app import app, db
from flask_mysqldb import MySQL
from app.models.tables import Pessoa
import folium


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
    result = cur.execute("SELECT * FROM fast_food_restaurants_us")

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


@app.route('/graficos')
def graficos():
    #create cursor
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM fast_food_restaurants_us ")

    lojas = cur.fetchall()
    return render_template('graficos.html', lojas=lojas)

@app.route('/mapa')
def make_chicago_map():

    cur = mysql.connection.cursor()

    #get article
    result1 = cur.execute("SELECT latitude FROM comercio_food where codigo  <= 4 ")
    
    result1 = cur.fetchone()

    resultudo = cur.fetchall()

    listByAge = [3]
    lista = []


    #Percorre a variavel do select e adiciona ao vetor lista
    for linha in resultudo:
        lista.append(linha)
        print("latitude:", linha )
    
    print(lista)

    #Maneira de eliminar a chave e obter o valor
    row = [listaq['latitude'] for listaq in lista]
    
    print(row)



        
    result = cur.execute("SELECT longitude FROM comercio_food where codigo = 2 ")
    

    result2 = cur.fetchone()

    
    print("VAlor> ")
    

    #pegar o valor key e value quando coloca fetchone()
    for k, v in result2.items():
        result2[k] = float(v)
        
    
    
    result = v
    result1 = 35.803788
    result = -83.580553
   
    
    folium_map = folium.Map(location=[result1, result],
                            zoom_start=14,
                            tiles="cartodbpositron",
                            width='75%', 
                            height='75%')
    folium.Marker(
    [result1, result], popup="<i>Mt. Hood Meadows</i>"
    ).add_to(folium_map)
    folium.Marker(
    [35.782339, -83.551408], popup="<b>Timberline Lodge</b>"
    ).add_to(folium_map)
    folium_map.save('app/templates/mapa.html')
    return render_template('mapa.html')