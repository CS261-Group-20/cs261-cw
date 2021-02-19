from flask import Flask, render_template, redirect
from forms import LoginForm, RegistrationForm, SessionCreationForm, SessionJoinForm, AttendeeForm, HostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '68279'


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
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
