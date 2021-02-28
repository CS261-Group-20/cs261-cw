from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import string
import random
from flask import Flask, render_template, redirect
from forms import LoginForm, RegistrationForm, SessionCreationForm, SessionJoinForm, AttendeeForm, HostForm
from models import db, users, eventTable, eventHosts
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '68279'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.db'
bootstrap = Bootstrap(app)
i = 1

with app.app_context():
    db.init_app(app)

@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    flash("This is a flashed message.")
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
                session["user_id"] = user.user_id
                flash('Welcome %s' % username_form)
                # return user.password
            else:
                flash('Invalid Login!')
    return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    i = users.query.order_by(users.user_id.desc()).first().user_id
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        new_user = users(i+1, username, pwd)
        db.session.add(new_user)
        db.session.commit()
        i += 1
        return "Yayyyy"
    return render_template("register.html", form = form)
    return render_template("register.html", form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    if "user_id" in session:
        user = users.query.filter_by(user_id=session["user_id"]).first()
        return str(session["user_id"])
    else:
        return "not logged in"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

@app.route('/session_create', methods=['GET', 'POST'])
def session_create():
    global i
    form = SessionCreationForm()
    if "user_id" in session: 
        if request.method == 'POST':
            session_name =  request.form['session_name']
            session_type =  request.form['session_type']
            session_start =  request.form['session_start']
            fmt = "%d-%m-%Y"
            dt_session_start = datetime.datetime.strptime(session_start, fmt)  
            session_end =  request.form['session_end'] 
            dt_session_end = datetime.datetime.strptime(session_end, fmt)
            session_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            new_session = eventTable(i,session_name,session_type,dt_session_start, dt_session_end, 0)
            db.session.add(new_session)
            # Add the user in session as the event host
            user_host = eventHosts(session["user_id"],i)
            db.session.add(user_host)
            db.session.commit()
            return "yay"
            i += 1
    else:
        return "You are not logged in!"
    return render_template("session_create.html", form=form)
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

# @app.route('/user', methods=['GET', 'POST'])
# def user():
#     results = []
#     events = eventTable.query.filter_by(event_id = 1).all()
#     return render_template("user.html")

if __name__ == "__main__":
    app.run(debug=True)
