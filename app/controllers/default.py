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

    ####OBTER VALOR LATITUDE
    #get latitude
    resultlati = cur.execute("SELECT latitude FROM comercio_food")

    resultlati = cur.fetchall()

    listaLati = []

             #Percorre a variavel do select e adiciona ao vetor lista

     #Percorre a lista de Latitude
    for linha in resultlati:
        listaLati.append(linha)
    



    #####OBTER VALOR LONGITUDE
     #Lista de longitude
    resultlong = cur.execute("SELECT longitude FROM comercio_food")

    resultlong = cur.fetchall()

    #Listas que será usado no mapa
    
    listaLongi = []

         #Percorre a variavel do select e adiciona ao vetor lista

    #Percorre a lista de Longitude
    for linha in resultlong:
        listaLongi.append(linha)
  


    
    #Lista nome do Restaurante
    resultname = cur.execute("SELECT name FROM comercio_food")
   
    resultname = cur.fetchall()

    listaNome = []

        #Percorre a variavel do select e adiciona ao vetor lista

    #Percorre a lista de nomes
    for linha in resultname:
        listaNome.append(linha)
   

   

    ####################################################
    

        #Maneira de eliminar a chave e obter o valor
    #obter o valor da Longitude
    listaLongi = [listaq['longitude'] for listaq in listaLongi]
   

    #obter valor da Latitude
    listaLati = [listaq['latitude'] for listaq in listaLati]
   
    
    listaNome = [listaq['name'] for listaq in listaNome]
    
  
    

    ####################################################### "NOja1:"


    #teste#print("NOja1:" + listaNome[1])

    contador = -1
    for n in listaNome:
        contador += 1
        loja1 = Lojas(listaNome[contador],listaLati[contador],listaLongi[contador])


    
    
    ###Teste
    result1 = 35.803788
    result = -83.580553
   

   ###############################################



   ################################################


    
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


    

    contador = -1
    for i in listaLongi:
        contador += 1
        folium.Marker(
        [listaLati[contador], listaLongi[contador] ], popup = listaNome[contador]
        ).add_to(folium_map)



    folium_map.save('app/templates/mapa.html')
    return render_template('mapa.html')

class Lojas:
    def __init__(self, nome, latitude, longitude):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude