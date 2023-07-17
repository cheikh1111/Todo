from flask import Blueprint, render_template, redirect
from datetime import datetime


# Creating main blueprint
views = Blueprint('Views', __name__)

# Creating routes

# 1. Creating home route
@views.route('/home')
@views.route('/')
def Home():
    return redirect('/todo')


# 2. about route
@views.route('/about')
def about():
    return render_template('about.html',title='About Us')

# handling 404 error(Page Not Found Error)
@views.app_errorhandler(404)
def handle_404(e):
    date = datetime.now()
    return render_template('404.html', date=date,title='404 Page Not Found')



