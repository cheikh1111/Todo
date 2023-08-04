from flask import Blueprint, render_template,session, redirect, request, flash, make_response
from werkzeug.security import generate_password_hash , check_password_hash
from sqlalchemy import or_
from . import db
from .models import User , Todo
from .forms import RegisterForm,LoginForm,TodoForm,ContactForm
import smtplib
from email.message import EmailMessage
from string import ascii_letters  , punctuation 
from dotenv import load_dotenv
from os import path,getenv
from datetime import datetime
# Main Blueprint
auth = Blueprint('authentication', __name__)


# Creating basic encryption and decryption functions 
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


# Creating Routes
# 1. Register route
@auth.route('/signup',methods=['GET' , 'POST'])
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Handling post request
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_confirmation = form.password_confirm.data
        email = form.email.data

        # Validating Password confirmation field manually
        if password != password_confirmation:
            flash('Password and Password confirmation must match',category='error')
            return redirect('/register')
        # Adding User to database
        else:
            user = not User.query.filter(or_(User.username==username , User.email == encrypt(email)))
            if not user:
                new_user = User(username=username,password=generate_password_hash(password,method='sha256'),email=encrypt(email))
                db.session.add(new_user)
                db.session.commit()
                db.session.close()
            else :
                flash('User already exists try again!',category='error')
                return redirect('/register')
        # Redirecting User
        return redirect('/login')
    
    return render_template('register.html', title='Create Account' , form = form )


# 2. Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Handling post request
    if form.validate_on_submit():
        # Getting username and password from form
        username = form.username.data
        password = form.password.data

        # Validating credentials
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password , password):
            flash("The provided credentials don't match our records" , category='error')
            return redirect('/login')
        
        # Remembering user and loging him
        else :
            session['user_id'] = user.id
            response = make_response(redirect('/todo'))
            response.set_cookie('user_id',str(user.id))
            return redirect('/todo')
    logged_in = 'user_id' in session
    return render_template("login.html", title='Login To Your Account', form=form ,logged_in=logged_in)




# 3. Todo Route
@auth.route('/Todo',methods=['GET','POST'])
@auth.route('/todo',methods=['GET','POST'])
def todo():
    form = TodoForm()
    if not 'user_id' in session :
        form = LoginForm()
        return redirect('/login')
    # handling POST Request44
    elif form.validate_on_submit() : 
        task = Todo(task=form.task.data,user_id=session['user_id'])
        db.session.add(task)
        db.session.commit()
        db.session.close()
    user_id = session['user_id']
    todo = [todo for todo in User.query.get(user_id).todos][::-1]
    
    return render_template('todo.html',title='Tasks' ,form = form , todo=todo , logged_in=True , user_id = user_id)

# 4. Contact route
@auth.route('/contact',methods=['GET','POST'])
def contact():
    if 'user_id' in session :
        form = ContactForm()
        if not 'user_id' in session : 
            return redirect('/login')
        
        if form.validate_on_submit():
            sender_mail = User.query.get(session['user_id']).email
            message = form.message.data
                
            # 1. Setting up email
            load_dotenv(path.dirname(__file__)+'/MAIL_INFO.env')        
            
            server = getenv('SERVER')
            port = getenv('PORT')
            mail = getenv('MAIL')
            password = getenv('PASSWORD')

            print(server)
            print(port)
            print(mail)
            print(password)
            Message = EmailMessage()
            Message.From = 'Message From Your Todo app'
            Message.Subject = 'Redirecting Message From Your app'
            Message.To = mail
            Message.set_content(f"Date : {datetime.now()} \nSender : {sender_mail} \n" + message ) 
        
            # Sending email 
            with smtplib.SMTP_SSL(server , port) as smtp :
                smtp.login(mail,password)
                smtp.send_message(mail,mail,message.as_string())
                smtp.quit()
        return render_template('contact.html',form= form , logged_in=True)

    return 'Please login to access this page' , 403

# 5. Login out Route
@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out',category='info')
    return redirect('/login')


# 6. Add todo 
@auth.route('/add-todo',methods=['POST'])
def add():
    todo = request.form.get('todo')
    user_id = request.form.get('user_id')
    if todo and user_id:
        todo = Todo(todo=todo,user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return {
                'status' : 200,
                'todo_id' : todo.id
              }

    return "Bad Request" , 400

# 7. Complete todo
@auth.route('/complete-todo',methods=['PUT'])
def complete():
    data = request.get_json()
    todo_id = data.get('todo_id',None)
    if todo_id :
        task = Todo.query.get(todo_id) 
        if task :
            task.complete =True
            db.session.commit()
            db.session.close()
            return 'Record Updated successfully! ' , 200

    return "Bad Request" , 400

# 8. Delete Todo
@auth.route('/delete-todo/<int:todo_id>',methods=['DELETE'])
def delete(todo):
    if todo:
        todo = Todo.query.get(todo)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            db.session.close()
            return 'Task deleted successfully! ' , 200
    return "Bad Request" , 400


# 9. Edit todo
@auth.route('/edit-todo',methods=['PUT'])
def edit():
    data = request.get_json()
    todo_id = data.get('todo_id',None)
    new_todo = data.get('todo',None)

    if todo_id and new_todo:
        todo= Todo.query.get(todo_id)
        if todo:
            todo.todo = new_todo
            db.session.commit()
            db.session.close()
            return "Todo edited successfully",200
    
    return "Bad Request" , 400

# 10. admin route
@auth.route('/admin')
def admin():
    user_id = session.get('user_id',None)
    if user_id:
        user = User.query.get(user_id)
        if user and user.admin:
            return render_template('admin.html',title='Admin Dashboard')

    return "You Aren't admin",403


