from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm, SessionCreationForm
from sqlalchemy.engine import create_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = '68279'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.db'

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template("register.html", form = form)

@app.route('/session_create')
def session_create():
    form = SessionCreationForm()
    return render_template("session_create.html", form = form)


@app.route('/host')
def host():
    return render_template("host.html")

@app.route('/attendee')
def attendee():
    return render_template("attendee.html")



if __name__ == "__main__":
    app.run(debug=True)