from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm, SessionCreationForm
from models import  db, users


app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = '68279'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.db'
i = 1

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

@app.route('/register', methods=['POST', 'GET'])
def register():
    global i
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        new_user = users(i, username, pwd)
        db.session.add(new_user)
        db.session.commit()
        i += 1
        return "Yayyyy"
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