from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/host')
def host():
    return render_template("host.html")

@app.route('/attendee')
def attendee():
    return render_template("attendee.html")

if __name__ == "__main__":
    app.run(debug=True)