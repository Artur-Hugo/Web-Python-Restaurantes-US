import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')  
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/db?host=localhost?port=3306'
SQLALCHEMY_TRACK_MODIFICATIONS = True

  #'sqlite:///' + os.path.join(basedir, 'banco.db')



