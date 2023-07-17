from . import db 
class User(db.Model):
    __tablename__ = 'user' # Name of the Table

    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String,unique = True)
    password = db.Column(db.String)
    todos = db.relationship('Todo', backref='user', lazy=True)


class Todo(db.Model):
    __tablename__ = 'Todo'

    id = db.Column(db.Integer,primary_key= True)
    task    = db.Column(db.String, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

