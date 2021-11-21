from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__) 
app.config.from_object('config')

#utilizaremos o flask para gerenciar o banco de dados db
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#para poder usar os comandos de SqLite
manager = Manager(app)
manager.add_command('db', MigrateCommand)








from app.controllers import default
