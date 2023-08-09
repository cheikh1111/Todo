from . import db 
from datetime import datetime


class User(db.Model):
    __tablename__ = 'User' # Name of the Table

    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String,unique = True)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    is_admin = db.Column(db.Boolean,nullable=False,default=False)
    todos = db.relationship('Todo', backref='User', lazy=True)


class Todo(db.Model):
    __tablename__ = 'Todo'

    id = db.Column(db.Integer,primary_key= True)
    todo   = db.Column(db.String, nullable=False) 
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    completed = db.Column(db.Boolean,default=False,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
