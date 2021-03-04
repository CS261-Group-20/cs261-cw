from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import date
import string
import random
from collections import namedtuple
from flask import Flask, render_template, redirect
from forms import LoginForm, RegistrationForm, SessionCreationForm, SessionJoinForm, AttendeeForm, HostForm
from models import db, users, eventTable, eventHosts, eventAttendees, feedbackQuestions, feedback
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '68279'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.db'
bootstrap = Bootstrap(app)

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
                return redirect('/user_homepage')
        flash('Invalid Login!')
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    user = users.query.order_by(users.user_id.desc()).first()
    if user:
        i = user.user_id
    else:
        i = 0
    form = RegistrationForm()
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        new_user = users(i+1, username, pwd)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html", form = form)


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
    # TODO : ADD DEFAULT QUESTION FOR EACH EVENT
    event = eventTable.query.order_by(eventTable.event_id.desc()).first()
    if event:
        i = event.event_id
    else:
        i = 0
    feedbackq_counter = feedbackQuestions.query.order_by(feedbackQuestions.feedback_question_id.desc()).first()
    if feedbackq_counter:
        j = feedbackq_counter.feedback_question_id
    else:
        j = 0
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
            new_session = eventTable(i + 1,session_name,session_type,dt_session_start, dt_session_end, session_code, 0)
            db.session.add(new_session)
            # Add the user in session as the event host
            user_host = eventHosts(session["user_id"],i + 1)
            db.session.add(user_host)
            db.session.commit()
            # Add a default question to the event
            default_question = feedbackQuestions(j + 1,"General Feedback", i + 1)
            db.session.add(default_question)
            db.session.commit()
            session["host_event_id"] = i + 1
            return redirect(url_for('host', id = session["host_event_id"]))
    else:
        return "You are not logged in!"
    return render_template("session_create.html", form=form)


@app.route('/session_join', methods=['GET', 'POST'])
def session_join():
    form = SessionJoinForm()
    if request.method == 'POST':
        session_code = request.form['session_code']
        event_joined = eventTable.query.filter_by(event_code = session_code).first()
        if event_joined:
            session["attendee_event_id"] = event_joined.event_id
            new_attendee = eventAttendees(session["user_id"],session["attendee_event_id"])
            db.session.add(new_attendee)
            db.session.commit()
            return redirect(url_for('attendee', id = session["attendee_event_id"]))
        else:
            return "Session code incorrect"
    return render_template("session_join.html", form=form)


@app.route('/host/<id>', methods=['GET', 'POST'])
def host(id):
    feedback_counter = feedbackQuestions.query.order_by(feedbackQuestions.feedback_question_id.desc()).first()
    if feedback_counter:
        j = feedback_counter.feedback_question_id
    else:
        j = 0

    event = eventTable.query.filter_by(event_id = id).first()

    form = HostForm()
    # Get list of all users in this session
    # TODO
    # Get attendees
    users_in_session = users.query.join(eventAttendees, users.user_id == eventAttendees.user_id).filter(eventAttendees.event_id == id).all()
    # Get host information
    user_host = users.query.filter_by(user_id = session["user_id"]).first()
    #
    # Display the feedback questions for the attendee
    questions_in_session = feedbackQuestions.query.filter_by(event_id = id).all()
    # TODO
    #

    if request.method == 'POST':
        question = request.form['add_feedback_question']
        new_question = feedbackQuestions(j + 1, question ,id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('host', id = id))
        

    return render_template("host.html", form=form, users_in_session = users_in_session, user_host = user_host, questions_in_session = questions_in_session, event = event )


@app.route('/attendee/<id>', methods=['GET', 'POST'])
def attendee(id):
    feedback_counter = feedback.query.order_by(feedback.feedback_id.desc()).first()
    if feedback_counter:
        j = feedback_counter.feedback_id + 1
    else:
        j = 1

    # Get list of all users in this session
    # TODO
    # Get attendees
    users_in_session = users.query.join(eventAttendees, users.user_id == eventAttendees.user_id).filter(eventAttendees.event_id == id).all()
    # Get host information
    user_host = users.query.join(eventHosts, users.user_id == eventHosts.user_id).filter(eventHosts.event_id == id).first()
    #

    # Get questions for the event
    questions_in_session = feedbackQuestions.query.filter_by(event_id = id).all()
    form_questions = []
    counter = 0
    for questions in questions_in_session:
        form_questions.append({"question_id": counter ,
        "question": counter})
        counter+=1
    
    form = AttendeeForm(feedback_questions = form_questions)
    counter = 0
    for questions in form.feedback_questions:
        questions.question.label.text = questions_in_session[counter].feedback_question
        questions.question_id = questions_in_session[counter].feedback_question_id
        counter+= 1

    if request.method == 'POST':
        #TODO: GET THIS TO WORK
        mood = request.form["mood_type"]
        for field in form["feedback_questions"]:
            message = field.question.data
            fmt = "%d-%m-%Y, %H:%M:%S"
            feedback_time = datetime.datetime.strptime(date.today().strftime("%d-%m-%Y, %H:%M:%S"), fmt)
            new_feedback = feedback(j, field.question_id, id, session["user_id"], message, feedback_time, 1 , 1,)
            db.session.add(new_feedback)
            db.session.commit()
            j += 1
        return redirect(url_for('attendee', id = id))


    return render_template("attendee.html", form=form, users_in_session = users_in_session, user_host = user_host, questions_in_session = questions_in_session, counter = counter)

@app.route('/user_homepage', methods=['GET', 'POST'])
def user_homepage():
    if "user_id" in session:
        events_host_user = eventTable.query.join(eventHosts, eventTable.event_id == eventHosts.event_id).filter(eventHosts.user_id == session['user_id']).all()
        events_attendee_user = eventTable.query.join(eventAttendees, eventTable.event_id == eventAttendees.event_id).filter(eventAttendees.user_id == session['user_id']).all()
        return render_template("user_homepage.html", events_host_user = events_host_user, events_attendee_user = events_attendee_user)
    else:
        # TODO: Redirect user to login 
        flash('Invalid Login!')
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
