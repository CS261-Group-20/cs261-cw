from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return("This is the Login Page")

@app.route('/host')
def host():
    return("This is the Host Page")

@app.route('/attendee')
def attendee():
    return("This is the Attendee Page")

if __name__ == "__main__":
    app.run(debug=True)