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
# from flask_bootstrap import Bootstrap
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from sentiment import processFeedbackData


app = Flask(__name__)
app.config['SECRET_KEY'] = '68279'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.db'
# bootstrap = Bootstrap(app)

with app.app_context():
    db.init_app(app)

# Default url route just redirects user to home webpage


# here we define our menu items


@app.route('/')
def index():
    return redirect('/home')

# Home url route renders the homepage


@app.route('/home')
def home():
    return render_template("home.html")

# Login url route handles user login


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # When a user submits a login request get the username and password from the form
    if request.method == 'POST':
        username_form = request.form['username']
        pwd = request.form['password']
        user = users.query.filter_by(username=username_form).first()

        # if username/password pair exist in database allow login and redirect user to user_homepage webpage,
        if user:
            if user.password == pwd:
                session["user_id"] = user.user_id
                flash('Welcome %s' % username_form)
                return redirect('/user_homepage')
        # else display invalid login message and prompt user for login again
        flash('Invalid Login!')
    return render_template("login.html", form=form)

# Register url route handles user registration


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Generate a new user_id one increment higher than the hightest existing user_id
    user = users.query.order_by(users.user_id.desc()).first()
    if user:
        i = user.user_id
    else:
        i = 0

    form = RegistrationForm()
    # When a user submits a registration request, get the username and passwords from the form, check for password consistency,
    # add user to database and redirect user to login page
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        confirmPwd = request.form['confirm_password']

        # Checking password consistency
        if confirmPwd != pwd:
            flash('Passwords do not match', category=Warning)
            return render_template("register.html", form=form)

        new_user = users(i+1, username, pwd)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html", form=form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    if "user_id" in session:
        user = users.query.filter_by(user_id=session["user_id"]).first()
        return str(session["user_id"])
    else:
        return "not logged in"

# Logout url route removes user from session and redirects user to homepage


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

# Session_create url route handles session creation


@app.route('/session_create', methods=['GET', 'POST'])
def session_create():
    # Generate a new event_id one increment higher than the hightest existing event_id
    event = eventTable.query.order_by(eventTable.event_id.desc()).first()
    if event:
        i = event.event_id
    else:
        i = 0

    # Generate a new feedback_question_id one increment higher than the hightest existing feedback_question_id
    feedbackq_counter = feedbackQuestions.query.order_by(
        feedbackQuestions.feedback_question_id.desc()).first()
    if feedbackq_counter:
        j = feedbackq_counter.feedback_question_id
    else:
        j = 0

    form = SessionCreationForm()
    # Allow session creation only if a user is logged in
    if "user_id" in session:
        # When user creates a new session, promt user for a session name, type, start date and end date
        if request.method == 'POST':
            session_name = request.form['session_name']
            session_type = request.form['session_type']
            session_start = request.form['session_start']
            session_end = request.form['session_end']
            fmt = "%d-%m-%Y"
            dt_session_start = datetime.datetime.strptime(session_start, fmt)
            dt_session_end = datetime.datetime.strptime(session_end, fmt)

            # Generate a random 8-character string to be used as session code and add new session to database
            session_code = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(8))
            new_session = eventTable(
                i + 1, session_name, session_type, dt_session_start, dt_session_end, session_code, 0)
            db.session.add(new_session)

            # Add the user in session as the event host
            user_host = eventHosts(session["user_id"], i + 1)
            db.session.add(user_host)
            db.session.commit()

            # Add a default question to the event
            default_question = feedbackQuestions(
                j + 1, "General Feedback", i + 1)
            db.session.add(default_question)
            db.session.commit()
            session["host_event_id"] = i + 1
            return redirect(url_for('host', id=session["host_event_id"]))
    else:
        flash('Not logged in!')
        return redirect(url_for('login'))
    return render_template("session_create.html", form=form)

# Session_join url route handles session joining


@app.route('/session_join', methods=['GET', 'POST'])
def session_join():
    form = SessionJoinForm()
    # Whenever a user submits a join session request, check whether that event code exists in the database
    if request.method == 'POST':
        session_code = request.form['session_code']
        event_joined = eventTable.query.filter_by(
            event_code=session_code).first()

        # If the event exists, add the user as an attendee to that session
        if event_joined:
            session["attendee_event_id"] = event_joined.event_id
            if "user_id" in session:
                new_attendee = eventAttendees(
                    session["user_id"], session["attendee_event_id"])
                attendee_in_session = eventAttendees.query.filter_by(
                    user_id=session["user_id"]).first()
                if not attendee_in_session:
                    db.session.add(new_attendee)
                    db.session.commit()
            return redirect(url_for('attendee', id=session["attendee_event_id"]))
        else:
            return "Session code incorrect"
    return render_template("session_join.html", form=form)

# host url route renders the host page and allows hosts to add additional questions to feedback form


@app.route('/host/<id>', methods=['GET', 'POST'])
def host(id):

    feedback_counter = feedback.query.filter_by(event_id=id).count()
    if feedback_counter != 0:
        values, labels, avg_score = processFeedbackData(id)
    else:
        avg_score = 0
        values = []
        labels = []
    print(id)
    feedback_time = labels
    feedback_mood = values
    positive_mood = []
    negative_mood = []

    for mood in feedback_mood:
        if mood >= 0:
            positive_mood.append(mood)
            negative_mood.append(None)
        else:
            positive_mood.append(None)
            negative_mood.append(mood)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=feedback_time, y=positive_mood,
                         marker_color='green', name='Positive<br>Feedback'))
    fig.add_trace(go.Bar(x=feedback_time, y=negative_mood,
                         marker_color='red', name='Negative<br>Feedback'))
    fig.update_layout(barmode='relative', title_text='Mood Over Time')
    fig.update_yaxes(range=[-1, 1])

    data = fig
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    # Generate a new feedback_question_id one increment higher than the hightest existing feedback_question_id
    feedback_counter = feedbackQuestions.query.order_by(
        feedbackQuestions.feedback_question_id.desc()).first()
    if feedback_counter:
        j = feedback_counter.feedback_question_id
    else:
        j = 0

    event = eventTable.query.filter_by(event_id=id).first()
    form = HostForm()

    # Get list of all attendees in this session
    users_in_session = users.query.join(eventAttendees, users.user_id == eventAttendees.user_id).filter(
        eventAttendees.event_id == id).all()
    # Get host information
    user_host = users.query.filter_by(user_id=session["user_id"]).first()
    # Display the feedback questions for the attendee
    questions_in_session = feedbackQuestions.query.filter_by(event_id=id).all()

    # Display all feedback for current session:
    feedback_in_session = feedback.query.join(users, users.user_id == feedback.user_id).join(feedbackQuestions,feedbackQuestions.feedback_question_id == feedback.feedback_question_id).add_columns(
        users.username, feedback.message, feedback.feedback_date, feedbackQuestions.feedback_question).filter(feedback.event_id == id).all()

    # When user submits a new question to be added to feedback form, add that queston to the database
    if request.method == 'POST':
        question = request.form['add_feedback_question']
        new_question = feedbackQuestions(j + 1, question, id)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('host', id=id))
    return render_template("host.html", form=form, users_in_session=users_in_session, user_host=user_host, questions_in_session=questions_in_session, event=event, feedback_in_session=feedback_in_session,
                           id=id, plot=graphJSON, title='Score over time', labels=labels, values=values, avg_score = avg_score )

# Attendee url route renders the attendee page and allows attendees to submit feedback


@app.route('/attendee/<id>', methods=['GET', 'POST'])
def attendee(id):
    # Generate a new feedback_id one increment higher than the hightest existing feedback_id
    feedback_counter = feedback.query.order_by(
        feedback.feedback_id.desc()).first()
    if feedback_counter:
        j = feedback_counter.feedback_id + 1
    else:
        j = 1

    # Get list of all users in this session
    # TODO
    # Get list of all attendees in this session
    users_in_session = users.query.join(eventAttendees, users.user_id == eventAttendees.user_id).filter(
        eventAttendees.event_id == id).all()
    # Get host information
    user_host = users.query.join(eventHosts, users.user_id == eventHosts.user_id).filter(
        eventHosts.event_id == id).first()

    # Get questions for the event
    questions_in_session = feedbackQuestions.query.filter_by(event_id=id).all()
    form_questions = []
    counter = 0
    for questions in questions_in_session:
        form_questions.append({"question_id": counter, "question": ''})
        counter += 1
    form = AttendeeForm(feedback_questions=form_questions)
    counter = 0
    for questions in form.feedback_questions:
        questions.question.label.text = questions_in_session[counter].feedback_question
        questions.question_id = questions_in_session[counter].feedback_question_id
        counter += 1

    # When a user submits feedback, store the feedback message and timestamp at which feedback was submitted
    if request.method == 'POST':
        mood = request.form["mood_type"]
        print("mood is", mood)
        if int(mood) == 2:
            mood = 0
        elif int(mood) == 3:
            mood = -1
        is_anon = request.form.get("checkbox", False)
        for field in form["feedback_questions"]:
            message = field.question.data
            fmt = "%d-%m-%Y, %H:%M:%S"
            feedback_time = datetime.datetime.strptime(
                datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"), fmt)
            if is_anon:
                new_feedback = feedback(
                    j, field.question_id, id, 0, message, feedback_time, mood, 1, 1)
            elif "user_id" in session:
                new_feedback = feedback(
                    j, field.question_id, id, session["user_id"], message, feedback_time, mood, 1, 0)
            else:
                new_feedback = feedback(
                    j, field.question_id, id, 0, message, feedback_time, mood, 1, 0)
            db.session.add(new_feedback)
            db.session.commit()
            j += 1
        return redirect(url_for('attendee', id=id))
    return render_template("attendee.html", form=form, users_in_session=users_in_session, user_host=user_host, questions_in_session=questions_in_session, counter=counter)

# The user_homepage url route provides the user with a list of all sessions in which the user is present as a host or as an attendee


@app.route('/user_homepage', methods=['GET', 'POST'])
def user_homepage():
    if "user_id" in session:
        events_host_user = eventTable.query.join(eventHosts, eventTable.event_id == eventHosts.event_id).filter(
            eventHosts.user_id == session['user_id']).all()
        events_attendee_user = eventTable.query.join(eventAttendees, eventTable.event_id == eventAttendees.event_id).filter(
            eventAttendees.user_id == session['user_id']).all()
        return render_template("user_homepage.html", events_host_user=events_host_user, events_attendee_user=events_attendee_user)
    # If user accesses user_homepage wile not logged in, redirect user to login page
    else:
        flash('Not logged in!')
        return redirect(url_for('login'))

# The user_homepage url route provides the user with a list of all sessions in which the user is present as a host or as an attendee


@app.route('/delete_question/<event_id>/<q_id>', methods=['GET', 'POST'])
def delete_question(event_id, q_id):
    # Remove the question from feedback_questions
    feedbackQuestions.query.filter_by(feedback_question_id=q_id).delete()
    # Remove any feedback which answers that question
    feedback.query.filter_by(feedback_question_id=q_id).delete()
    db.session.commit()
    return redirect(url_for('host', id=event_id))


# Run app
if __name__ == "__main__":
    app.run(debug=True)
