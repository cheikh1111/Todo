from flask import Blueprint , session , render_template
from datetime import datetime
from . import db
from .models import User,Todo
from string import ascii_letters, punctuation

admin = Blueprint('Dashboard',__name__)

characters = list(ascii_letters+punctuation) + [str(i) for i in range(10)]

def mix(list):
    list = list[::-1]
    for i in range(len(list) - 1):
        if i+1 == len(list):
            list[i] = list[i-1]
        else:
            list[i] = list[i+1]
    return list


mixed_chars = characters.copy()
mixed_chars = mix(mixed_chars)

def encrypt(key:str):
    return ''.join([mixed_chars[characters.index(char)] for char in key])
def decrypt(key:str):
    return ''.join([characters[mixed_chars.index(char)] for char in key])

@admin.route('/')
def Dashboard():
    user_id = session.get('user_id',None)
    if user_id:
        user = User.query.get(user_id)
        if user and user.is_admin:
            
            Users = User.query.all()
            Todos = Todo.query.all()
            return render_template('admin.html',title='Admin Dashboard',
                                   admin=True,users_num = len(Users),
                                   todos_num = len(Todos),date=datetime.now())
    return "<h1>403 Forbidden</h1>",403

@admin.route('/users')
def users():
    user_id = session.get('user_id',None)
    if user_id:
        user = User.query.get(user_id)
        if user and user.is_admin:          
            Users = User.query.all()
            for user in Users :
                user.email = decrypt(user.email)
            return render_template('users.html',title='Admin Dashboard',
                                   admin=True, Users = Users)
    return "<h1>403 Forbidden</h1>",403


@admin.route('/todos')
def todos():
    user_id = session.get('user_id',None)
    if user_id:
        user = User.query.get(user_id)
        if user and user.is_admin:          
            Todos = Todo.query.all()

            return render_template('todos.html',title='Admin Dashboard',
                                   admin=True, Todos = Todos)
    return "<h1>403 Forbidden</h1>",403
