from flask import Blueprint,jsonify,abort, render_template,session, redirect, request, flash 
from werkzeug.security import generate_password_hash , check_password_hash
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
auth = Blueprint('authantication', __name__)


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
            
            new_user = User(username=username,password=generate_password_hash(password,method='sha256'),email=encrypt(email))
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
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
        if not user or not check_password_hash(user.password,password) :
            flash("The provided credentials don't match our records" , category='error')
            return redirect('login')
        
        # Remembering user and loging him
        else :
            session['user_id'] = user.id
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
    
    return render_template('todo.html',title='Start Organizing your day and add your day tasks' ,form = form , todo=todo , logged_in=True , user_id = user_id)

# 4. delete task route
@auth.route('/delete-todo' , methods = ['GET','POST'])
def delete_task():
    if  not 'user_id' in session:
        abort(404)
    if not request.method == 'POST':
        task_id = request.args.get('todo_id',None)
        if session.get('user_id',None) == Todo.query.get(task_id).user_id:
            task = Todo.query.get(task_id)
            db.session.delete(task)
            db.session.commit()
            db.session.close()
            return jsonify({})
        else: 
            abort(404)
    else : 
        abort(404)

# 5. contact route 


@auth.route('/contact',methods=['GET','POST'])
def contact():
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
        user =  getenv('USER')
        target = getenv('TARGET')
        password = getenv('PASSWORD')

        print(server)
        print(port)
        print(user)
        print(password)
        Message = EmailMessage()
        Message.From = 'Message From Your Todo app'
        Message.Subject = 'Redirecting Message From Your app'
        Message.To = target
        Message.set_content(f"Date : {datetime.now()} \nSender : {sender_mail} \n" + message ) 
    
        # Sending email 
        with smtplib.SMTP_SSL(server , port) as smtp :
            smtp.login(target,password)
            smtp.send_message(user,target,message.as_string())
            smtp.quit()
    return render_template('contact.html',form= form , logged_in=True)

# 6. api route
@auth.route('/api')
def api():
    
    if request.method == 'GET' and 'username' in  request.args and 'password' in request.args :
        user = User.query.filter_by(username=request.args['username']).first()
        if user :
            if check_password_hash(user.password , request.args['password']):
                todos = user.todos
                todos = {id + 1 :todo.task for id , todo in enumerate(todos)}
                return jsonify(todos)
    return abort(404)

# 7. Login out Route
@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out',category='info')
    return redirect('/login')
