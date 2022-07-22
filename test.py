from book_model import Accounts, db , Book 



def generateSchema():
    db.create_all() #create the schemas

# generateSchema()

def addSampleBook():
    p = Accounts()
    db.session.add(p) 
    db.session.commit() 

    repo = Accounts.query.filter_by(accId=1).first()
    if repo.issuedBooks != None :
        data = list(repo.issuedBooks)
        data.append({'name': 'Jessica', 'id': 12941, 'views': 12})
        repo.issuedBooks = data 
        db.session.add(repo) 

        db.session.commit() 
    else :
        data = []
        data.append({'name': 'Jessica', 'id': 12941, 'views': 12})
        repo.issuedBooks = data 
        db.session.add(repo) 

        db.session.commit() 


addSampleBook()


def display_books():
    print(Book.query.all())
    listt = []
    for b in Book.query.all():
        listt.append(b.json())
    print(listt)


display_books()