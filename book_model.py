from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    publication = db.Column(db.Text)
    isIssued = db.Column(db.Text) 
    issuedBy = db.Column(db.Text) 

    
    def json(self):
        return {'id' : self.id ,'name': self.name , 'author' : self.author , 'isIssued' : self.isIssued , "issuedBy" : self.issuedBy} 


class Libriarn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text )
    roll = db.Column(db.Text)

    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text )
    roll = db.Column(db.Text)

    
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text )
    roll = db.Column(db.Text)

class Accounts(db.Model):
    accId = db.Column(db.Integer, primary_key=True)
    issuedBooks = db.Column(db.PickleType)

    

