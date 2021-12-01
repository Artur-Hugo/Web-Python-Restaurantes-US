from flask import render_template, request
from flask.helpers import send_file
from geopy.exc import GeocoderTimedOut
from app import app, db
from flask_mysqldb import MySQL
from app.models.tables import Comercio
import folium
import pycep_correios
from geopy.geocoders import Nominatim
from pycep_correios import get_address_from_cep, WebService

app.debug = True

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b6011ef164691f'
app.config['MYSQL_PASSWORD'] = 'cf5067ed'
app.config['MYSQL_NAME'] = 'heroku_83a43c24789611f'
app.config['MYSQL_DB'] = 'heroku_83a43c24789611f'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

@app.route('/')
@app.route('/listagem', methods=['GET'])
def listagem():
    
    #create cursor
    cur = mysql.connection.cursor()

    cur.execute("select distinct province from comercio_food")

    conteudoProvince = cur.fetchall()

    #get articles
    result = cur.execute("SELECT * FROM comercio_food")


    conteudo = cur.fetchall()

    
    return render_template('listagem.html',restaurants=conteudo, province=conteudoProvince)




    
@app.route('/selecao/<int:id>')
def selecao(id=0):
    #create cursor
    cur = mysql.connection.cursor()

    #get article
    result = cur.execute("SELECT * FROM pessoas WHERE id = %s",[id])

    conteudo = cur.fetchone()


    
    return render_template('listagem.html', restaurants=conteudo)

@app.route('/consultar' , methods=['POST'])
def consulta():
    consulta = '%'+request.form.get('consulta')+'%'
    
    campo = request.form.get('campo')

    cur = mysql.connection.cursor()

    if campo == 'name':
        result = cur.execute("select * from comercio_food where name like %s",[consulta])
        result = cur.fetchall()
    elif campo == 'address':
        result = cur.execute("select * from comercio_food where address like %s",[consulta])
        result = cur.cur.fetchall()
    elif campo == 'city':
        result = cur.execute("select * from comercio_food where city like %s",[consulta])
        result = cur.fetchall()
    elif campo == 'province':
        result = cur.execute("select * from comercio_food where province like %s",[consulta])
        result = cur.fetchall()
    else:
        result = cur.execute("SELECT * FROM comercio_food")
    

    return render_template('listagem.html', restaurants=result)



@app.route('/insercao')
def insercao():

    cur = mysql.connection.cursor()


    #get articles
    cur.execute("SELECT * FROM comercio_food")


    conteudo = cur.fetchall()

    return render_template('insercao.html',province=conteudo)


@app.route('/salvar_insercao', methods=['POST'])

def salvar_insercao():
    form = Comercio(request.form)
    name = form.name.data
    address = form.address.data
    categories = form.categories.data
    city = form.city.data
    country = form.country.data
    latitude = form.latitude.data
    longitude = form.longitude.data
    postalCode = form.postalCode.data
    province = form.province.data
    
    

    cur = mysql.connection.cursor()

    #get articles
    cur.execute("INSERT INTO pessoas(name, address, categories, city, country, latitude, longitude,postalCode, province) VALUES(%s,%s,%s,%s,%s, %d,%d, %d, %s)",(name, address, categories, city, country, latitude,longitude, postalCode, province))

    # commit to DB
    mysql.connection.commit()
    #close connection
    conteudo = cur.fetchone()
    cur.close()

    

    return render_template('insercao.html', restaurants=conteudo)


@app.route('/graficos')
def graficos():
    #create cursor
    cur = mysql.connection.cursor()

    #get articles
    result = cur.execute("SELECT * FROM fast_food_restaurants_us ")

    lojas = cur.fetchall()
    return render_template('graficos.html', lojas=lojas)


@app.route('/Pesquisar/<int:codigo>')
def delecao(codigo=0):
    pesquisa = request.form.get('pesquisa')
    
    
     #create cursor
    cur = mysql.connection.cursor()

    
   
    ####OBTER VALOR LATITUDE
    #get latitude
    resultlati = cur.execute("""SELECT latitude FROM comercio_food where codigo = %s """, [codigo])
    resultlati = cur.fetchone()
    for k, latitude in resultlati.items():
        resultlati[k] = float(latitude)
    resultlongi = cur.execute("""SELECT longitude FROM comercio_food where codigo = %s """, [codigo])
    resultlongi = cur.fetchone()
    for k, longitude in resultlongi.items():
        resultlongi[k] = float(longitude)

    
    resultname = cur.execute("""SELECT name FROM comercio_food where codigo = %s """, [codigo])
    resultname = cur.fetchone()    
    for k, name in resultname.items():
        resultname[k] = str(name)
    
    

    ###Teste
    result1 = 35.803788
    result = -83.580553
   
    print("latitude:")
    print(latitude)
    print("longitude:")
    print(longitude)
    
    folium_map = folium.Map(location=[latitude, longitude ],
                            zoom_start=15,
                            tiles="cartodbpositron",
                            width='75%', 
                            height='75%',
                            position='relative',
                            left='12.5%' 
                            
                            )
    folium.Marker(
    [latitude, longitude], popup=name
    ).add_to(folium_map)
      


    folium_map.save('app/templates/mapa.html')


     #get articles
    cur.execute("SELECT * FROM comercio_food where codigo = %s ", [codigo])

    conteudo = cur.fetchall()



    return render_template('comerciopesquisado.html', pesquisa=codigo, conteudo=conteudo)

@app.route('/listagem' , methods=['POST'])
def make_province_map():

     #create cursor
    cur = mysql.connection.cursor()

    cur.execute("select distinct province from comercio_food order by province")

    conteudoProvince = cur.fetchall()


    listagem()
    
    estado = request.form.get('province11')
    estadocomaspas = '%'+request.form.get('province11')+'%'
    print("Estado: ")
    print(estado)
    cur = mysql.connection.cursor()

    cur.execute("select * from comercio_food where province like %s",[estadocomaspas])

    conteudo = cur.fetchall()

    ####OBTER VALOR LATITUDE
    #get latitude
    resultlati = cur.execute("SELECT latitude FROM comercio_food where province like %s",[estado])

    resultlati = cur.fetchall()

    listaLati = []

             #Percorre a variavel do select e adiciona ao vetor lista

     #Percorre a lista de Latitude
    for linha in resultlati:
        listaLati.append(linha)
    



    #####OBTER VALOR LONGITUDE
     #Lista de longitude
    resultlong = cur.execute("SELECT longitude FROM comercio_food where province like %s",[estado])

    resultlong = cur.fetchall()

    #Listas que será usado no mapa
    
    listaLongi = []

         #Percorre a variavel do select e adiciona ao vetor lista

    #Percorre a lista de Longitude
    for linha in resultlong:
        listaLongi.append(linha)
  


    
    #Lista nome do Restaurante
    resultname = cur.execute("SELECT name FROM comercio_food where province like %s",[estado])
   
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
    ####teste que não deu certo
    ##contador = -1
    ##for n in listaNome:
    ##    contador += 1
    ##    loja1 = Lojas(listaNome[contador],listaLati[contador],listaLongi[contador])


    
    
    ###Teste
    result1 = 35.803788
    result = -83.580553
   

   ###############################################



   ################################################


    
    folium_map = folium.Map(location=[result1, result],
                            zoom_start=5,
                            tiles="cartodbpositron",
                            width='75%', 
                            height='75%',
                            position='relative',
                            left='12.5%' 
                            
                            )
    #folium.Marker(
    #[result1, result], popup="<i>Mt. Hood Meadows</i>"
    #).add_to(folium_map)
    #folium.Marker(
    #[35.782339, -83.551408], popup="<b>Timberline Lodge</b>"
    #).add_to(folium_map)


    

    contador = -1
    print(len(listaLongi))
    for i in listaLongi:
        contador += 1
        folium.Marker(
        [listaLati[contador], listaLongi[contador] ], popup = listaNome[contador]
        ).add_to(folium_map)



    folium_map.save('app/templates/mapa.html')
    
    return render_template('listagem.html', estado=estado,restaurants=conteudo, province=conteudoProvince)


@app.route('/teste')
def testeTT():    
    return render_template('teste.html')

@app.route('/teste22',methods=['POST','GET'] )
def teste_map():
    
    cep = request.form.get('cep')
    print("CEP:")
    print(cep)
    address = request.form.get('address')
    print("address:")
    print(address)

    #geolocator = Nominatim(user_agent="geolocalização")
    #location = geolocator.geocode(address)
    
    #location = geolocator.geocode("R. Capote Valente, 39 - Pinheiros, São Paulo - SP, 05409-000")
    #location = geolocator.geocode("R. Rui Boto de Souza, 102 - Jardim Aracati, São Paulo - SP, 04949-020")
    #except ValueError:
    locatilati = -23.5525439
    locallongi = -46.6791195
    #print(location)
    
    print(cep)
    print("cep<<")


    # R. Dragão do Mar, 81 - Praia de Iracema, Fortaleza - CE, 60060-390
    # R. Capote Valente, Pinheiros - São Paulo
    # R. Dragão do Mar, 81 - Praia de Iracema, Fortaleza - CE, 60060-390
    geolocator = Nominatim(user_agent="geolocalização")
    location = geolocator.geocode("Av. Vítor Manzini, 450 - Santo Amaro, São Paulo - SP, 04745-060")
    print(location)
    
    #print(location.latitude)
    
    folium_map = folium.Map(location=[location.latitude, location.longitude ],
                        zoom_start=15,
                        tiles="cartodbpositron",
                        width='50%', 
                        height='50%',
                        position='relative',
                        left='12.5%' 
                        
                        )
    folium.Marker(
    [location.latitude, location.longitude], popup="<b>Timberline Lodge</b>"
    ).add_to(folium_map)
    


    folium_map.save('app/templates/mapa.html')


    

    print("tratado:")
    
    
    

    
    #print(location.longitude)
    #if(address == None):
    #    endereco = pycep_correios.get_address_from_cep(cep)

    #    geolocator = Nominatim(user_agent="test_app")
    #    location = geolocator.geocode(endereco['logradouro'] + ", " + endereco['cidade'] + " - " + endereco['bairro'])


    
    #print(location.latitude)

    #folium_map = folium.Map(location=[location.latitude, location.longitude ],
    #                        zoom_start=15,
    #                        tiles="cartodbpositron",
    #                        width='50%', 
    #                        height='50%',
    #                        position='relative',
    #                        left='12.5%' 
    #                        
    #                        )
    #folium.Marker(
    #[location.latitude, location.latitude], popup="Nome"
    #).add_to(folium_map)
      


    #folium_map.save('app/templates/mapa.html')

    return render_template('insercao.html')

class Lojas:
    def __init__(self, nome, latitude, longitude):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude

