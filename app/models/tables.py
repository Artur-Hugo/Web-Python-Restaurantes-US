from flask_mysqldb import MySQL
from app import app
from wtforms import Form, StringField , IntegerField, FloatField, validators



class Comercio(Form):
    name = StringField('name',[validators.Length(min=1,max=50)])
    address = StringField('address',[validators.Length(min=1,max=255)])
    categories = StringField('categories',[validators.Length(min=1,max=255)])
    city = StringField('city',[validators.Length(min=1,max=255)])
    province = StringField('province',[validators.Length(min=1,max=2)])
    country = StringField('country',[validators.Length(min=1,max=2)])
    latitude = FloatField('latitude')
    longitude = FloatField('longitude')
    postalCode = IntegerField('postalCode')
    websites = StringField('websites')