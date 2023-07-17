from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField,TextAreaField
from wtforms.validators import InputRequired , Length


# 1. LoginForm  
class LoginForm(FlaskForm):
    username = StringField('Username : ',validators=[InputRequired('Please fill out this field'),Length(min=2,max=25,message='The field lenght must be in the following range 2~20')],render_kw={'placeholder': 'Username'})
    password = PasswordField('Password : ' ,validators=[InputRequired('Please fill out this field'),Length(min=2,max=25,message='The field lenght must be in the following range 2~20')] ,render_kw={'Placeholder' : 'Password','class':'PasswordInput'})
    submit   = SubmitField('Login')
# 2.SignupForm
class RegisterForm(FlaskForm) :
    username = StringField('Username : ',validators=[InputRequired('Please fill out this field'),Length(min=2,max=25,message='The field lenght must be in the following range 2~20')],render_kw={'placeholder': 'Username'})
    password = PasswordField('Password : ' ,validators=[InputRequired('Please fill out this field'),Length(min=2,max=25,message='The field lenght must be in the following range 2~20')] ,render_kw={'Placeholder' : 'Password'})
    password_confirm = PasswordField('Confirm Password :' ,validators=[InputRequired('Please fill out this field')],render_kw={'placeholder': 'Confirm Password'} )
    email = EmailField('Email :',render_kw={'placeholder': 'Email'} ,validators=[InputRequired('Please fill out this field')] )
    submit = SubmitField('Submit')

# 3. TodoForm
class TodoForm(FlaskForm):
    task = StringField(' Add New Task : ' ,render_kw={'placeholder' : 'Task'},validators=[InputRequired('Please fill out this field')])
    submit = SubmitField('Add')


# 4. Contact form 
class ContactForm(FlaskForm):
    message = TextAreaField('Message : ',validators=[InputRequired('Please fill out message field'),Length(min=6)],render_kw={'placeholder':'Message'})
    email = EmailField('Email (optional) : ',render_kw={'placeholder':'email'})
    submit  = SubmitField('Send') 