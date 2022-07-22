#file path
import os

from flask import Flask 

app = Flask(__name__) 

projectDir = os.path.dirname(os.path.abspath(__file__))

print("Dir Path is" , projectDir)


dbFile = "sqlite:///{}".format(os.path.join(projectDir,"library.db"))

print("DataBase file is" , dbFile)

app.config['SQLALCHEMY_DATABASE_URI'] = dbFile

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =False
