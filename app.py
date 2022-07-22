
from settings import app
from book_model import Book, Libriarn , Admin , Customer 
from book_model import db 
import bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# Expetions for sqlaclemy
from sqlalchemy.exc import IntegrityError


from flask import request , jsonify , redirect , flash , session 

# Setup the Flask-JWT-Extended extension. Read more: https://flask-jwt-extended.readthedocs.io/en/stable/options/
app.config['JWT_SECRET_KEY'] = 'secret-secret'  # Change this!
jwt = JWTManager(app)


@app.route('/addBooks' , methods = ['POST'])
@jwt_required()
def addBooks():
    user = get_jwt_identity()
    roll = user['roll'] 
    if roll != "Libriarn" :
        return "Only Libriarn Can Do This" 
    r = request.get_json()
    name = r["name"]
    author = r["author"]
    description = r["description"]
    publication = r["publication"]
    book = Book(name = name , author = author , description = description , publication = publication , isIssued = "No" , issuedBy = "-")
    db.session.add(book) 
    db.session.commit() 
    return "Added" 


@app.route('/allBooks' , methods = ['GET'])
def allBooks():
    listt = []
    for b in Book.query.all():
        listt.append(b.json())
    print(listt)
    return jsonify(listt) 


@app.route('/deleteBook' , methods = ['DELETE'])
@jwt_required()
def deleteBook():
    token = get_jwt_identity()
    tokenRoll = token['roll']
    if tokenRoll != "Libriarn" :
        return "Only Librarian Can Do this"
    r = request.get_json()
    id = r["id"]
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return "deleted"


@app.route('/updateBook' , methods = ['POST'])
@jwt_required()
def updateBook():
    token = get_jwt_identity()
    tokenRoll = token['roll']
    if tokenRoll != "Libriarn" :
        return "Only Librarian Can Do this"
    r = request.get_json()
    id = r["id"]
    book = Book.query.filter_by(id=id).first()
    name = r["name"]
    author = r["author"]
    description = r["description"]
    publication = r["publication"]

    book.name = name
    book.author = author
    book.description = description 
    book.publication = publication 

    db.session.commit()
    return "updated"



@app.route('/issueBook' , methods = ['POST'])
@jwt_required()
def issueBook():
    token = get_jwt_identity()
    tokenRoll = token['roll']
    if tokenRoll != "Customer" :
        return "Not a customer"
        
    tokenEmail = token['email']

    r = request.get_json()
    id = r["id"]
    book = Book.query.filter_by(id=id).first()

    if book.isIssued == "Yes" :
        return jsonify({"message" : "Book already Issued"})

    book.isIssued = "Yes" 
    book.issuedBy = tokenEmail 
    
    db.session.commit()
    return "issued"


@app.route('/checkAccount' , methods = ['POST'])
@jwt_required()
def checkAccount():
    token = get_jwt_identity()
    tokenRoll = token['roll']
    if tokenRoll != "Customer" :
        return "Not a customer"
        
    tokenEmail = token['email']

    book = Book.query.filter_by(issuedBy = tokenEmail)

    listt = []
    for b in book:
        listt.append(b.json())
    print(listt)
    
    return jsonify(listt)

@app.route('/returnBook' , methods = ['POST'])
@jwt_required()
def returnBook():
    token = get_jwt_identity()
    tokenRoll = token['roll']
    if tokenRoll != "Customer" :
        return "Not a customer"
        
    tokenEmail = token['email']

    r = request.get_json()
    id = r["id"]
    book = Book.query.filter_by(id=id).first()

    if book.issuedBy != tokenEmail:
        return {"message" : "You dont have any such book"}

    book.isIssued = "No" 
    book.issuedBy = "-" 
    
    db.session.commit()
    return "returned"


@app.route('/register', methods=['POST'])
def register():
    try:
        # id = db.Column(db.Integer, primary_key=True)
        # email = db.Column(db.Text, unique=True, nullable=False)
        # hash = db.Column(db.Text, nullable=False)
        # name = db.Column(db.Text )
        # roll = db.Column(db.Text)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        name = request.json.get('name', None)
        roll = request.json.get('roll', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if roll == "Libriarn":
            user = Libriarn( email=email, hash=hashed , name = name , roll = roll )
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity={"email" : email , "roll" : roll})
            return {"access_token": access_token}, 200
        elif roll == "Admin" :
            user = Admin( email=email, hash=hashed , name = name , roll = roll )
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity={"email" : email , "roll" : roll})
            return {"access_token": access_token}, 200
        else :
            return {"message" : "Only Admins and Libriarn Can be Created"} 
    except IntegrityError:
        db.session.rollback()
        return 'User Already Exists', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@app.route('/registerCustomer', methods=['POST'])
@jwt_required()
def registerCustomer():
    try:
        # id = db.Column(db.Integer, primary_key=True)
        # email = db.Column(db.Text, unique=True, nullable=False)
        # hash = db.Column(db.Text, nullable=False)
        # name = db.Column(db.Text )
        # roll = db.Column(db.Text)
            
        token = get_jwt_identity()
        tokenEmail = token['roll']
        if tokenEmail != "Admin" :
            return {"message" : "Only Admins Can add Users"}

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        name = request.json.get('name', None)
        roll = request.json.get('roll', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if roll == "Customer":
            user = Customer( email=email, hash=hashed , name = name , roll = roll )
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity={"email" : email , "roll" : roll})
            return {"access_token": access_token}, 200
        else :
            return {"message" : "Error Occoured"}  
    except IntegrityError:
        db.session.rollback()
        return 'User Already Exists', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400







@app.route('/loginLibriarn', methods=['POST'])
def loginLibriarn():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        user = Libriarn.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404
        
        if bcrypt.checkpw(password.encode('utf-8'), user.hash):
            access_token = create_access_token(identity={"email": email , "roll" : user.roll})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@app.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        user = Admin.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404
        
        if bcrypt.checkpw(password.encode('utf-8'), user.hash):
            access_token = create_access_token(identity={"email": email , "roll" : user.roll})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400



@app.route('/loginCustomer', methods=['POST'])
def loginCustomer():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        user = Customer.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404
        
        if bcrypt.checkpw(password.encode('utf-8'), user.hash):
            access_token = create_access_token(identity={"email": email , "roll" : user.roll})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


# protected test route
@app.route('/test', methods=['GET'])
@jwt_required()
def test():
    user = get_jwt_identity()
    email = user['email']
    return f'Welcome to the protected route {email}!', 200

