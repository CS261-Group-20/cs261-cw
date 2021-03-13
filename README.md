# README

Code for our CS261 Coursework
![enter image description here](https://github.com/CS261-Group-20/cs261-cw/blob/main/home.PNG?raw=true)![enter image description here](https://github.com/CS261-Group-20/cs261-cw/blob/main/host_page.PNG?raw=true)![enter image description here](https://github.com/CS261-Group-20/cs261-cw/blob/main/create_session.PNG?raw=true)
![enter image description here](https://github.com/CS261-Group-20/cs261-cw/blob/main/attendee.PNG?raw=true)

## Installation Instructions

### Necessary modules

Install these Python modules

    pip install flask
    pip install flask_sqlalchemy
    pip install flask_sqlalchemy
    pip install plotly
    pip install textblob
    pip install rake_nltk
If possible install sqlite3 to access the database

If pip install does not work, try 'pip3 install'

### Running the app

Simply clone the repository and then run app.py and the website should be running on `http://127.0.0.1:5000/`

    py app.py

If that does not work, try 'python app.py' or 'python3 app.py'

### Using the app

Running the app will bring you to the homepage.

From there you will have the option to Register, Login, Create a session, Join a session or go to the user homepage (which shows all sessions currently joined both as a host and attendee)

A session can be joined without logging in, all you need is the session code.
However login is required to host a session or access the user homepage.

Once you host a session you will see the session code on the screen and from there it's just about receiving and looking at feedback.
