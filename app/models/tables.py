from flask_mysqldb import MySQL
from app import app
from wtforms import Form, StringField , IntegerField, FloatField, validators



class Pessoa(Form):
    nome = StringField('nome',[validators.Length(min=1,max=50)])
    idade = IntegerField('idade')
    sexo = StringField('sexo',[validators.Length(min=1,max=1)])
    salario = FloatField('salario')