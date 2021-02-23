from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm, SessionCreationForm
from models import  db, users

from flask import Flask, render_template, redirect
from forms import LoginForm, RegistrationForm, SessionCreationForm, SessionJoinForm, AttendeeForm, HostForm

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username_form = request.form['username']
        pwd = request.form['password']
        user = users.query.filter_by(username=username_form).first()
        if user:
            if user.password == pwd:
                return user.password
            else:
                return '<h1>Invalid username or password</h1>'
    return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
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
    return render_template("register.html", form=form)


@app.route('/session_create', methods=['GET', 'POST'])
def session_create():
    form = SessionCreationForm()
    return render_template("session_create.html", form=form)


@app.route('/session_join', methods=['GET', 'POST'])
def session_join():
    form = SessionJoinForm()
    return render_template("session_join.html", form=form)


@app.route('/host', methods=['GET', 'POST'])
def host():
    form = HostForm()
    return render_template("host.html", form=form)


@app.route('/attendee', methods=['GET', 'POST'])
def attendee():
    form = AttendeeForm()
    return render_template("attendee.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
