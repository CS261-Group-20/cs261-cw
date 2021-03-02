from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.sql.schema import PrimaryKeyConstraint
db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}, {self.password}>"


class eventTable(db.Model):
    __tablename__ = 'eventTable'

    event_id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_desc = db.Column(db.String(30), nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    event_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_code = db.Column(db.String(10), nullable=False)
    event_completed = db.Column(db.Integer, nullable=False)

    def __init__(self, event_id, event_desc, event_type, event_start, event_end, event_code, event_completed):
        self.event_id = event_id
        self.event_desc = event_desc
        self.event_type = event_type
        self.event_start = event_start
        self.event_end = event_end
        self.event_code = event_code
        self.event_completed = event_completed

    def __repr__(self):
        return f"<Event {self.event_id}, {self.event_desc}, {self.event_type}, {self.event_start}, {self.event_end}, {self.event_code}, {self.event_completed}>"

class eventAttendees(db.Model):
    __tablename__ = 'eventAttendees'

    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('eventTable.event_id'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'event_id'),{},)

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f"<Event Attendee {self.user_id},{self.event_id}>"

class eventHosts(db.Model):
    __tablename__ = 'eventHosts'

    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('eventTable.event_id'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'event_id'),{},)
    
    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f"<Event Host {self.user_id},{self.event_id}>"

class feedbackQuestions(db.Model):
    __tablename__ = 'feedbackQuestions'

    feedback_question_id = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback_question = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('eventTable.event_id'), nullable=False)

    def __init__(self, feedback_question_id, feedback_question, event_id):
        self.feedback_question_id = feedback_question_id
        self.feedback_question = feedback_question
        self.event_id = event_id

    def __repr__(self):
        return f"<Feedback Question {self.feedback_question_id}, {self.feedback_question}, {self.event_id}>"        

class feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback_question_id = db.Column(db.Integer, db.ForeignKey('feedbackQuestions.feedback_question_id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('eventTable.event_id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    message = db.Column(db.String(300), nullable=False)
    feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mood = db.Column(db.Float, nullable=False)
    sentiment = db.Column(db.Float, nullable=False)

    def __init__(self, feedback_id, feedback_question_id, event_id, user_id, message, feedback_date, mood, sentiment):
        self.feedback_id = feedback_id
        self.feedback_question_id = feedback_question_id
        self.event_id = event_id
        self.user_id = user_id
        self.message = message
        self.feedback_date = feedback_date
        self.mood = mood
        self.sentiment = sentiment

    def __repr__(self):
        return f"<Feedback {self.feedback_id},{self.feedback_question_id},{self.event_id},{self.user_id},{self.message},{self.user_id},{self.feedback_date},{self.mood},{self.sentiment}>"
