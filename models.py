from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


class eventTable(db.Model):
    __tablename__ = 'eventTable'

    event_id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_desc = db.Column(db.String(30), nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    event_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_completed = db.Column(db.Integer, nullable=False)

    def __init__(self, event_id, event_desc, event_type, event_start, event_end, event_completed):
        self.event_id = event_id
        self.event_desc = event_desc
        self.event_type = event_type
        self.event_start = event_start
        self.event_end = event_end
        self.event_completed = event_completed

    def __repr__(self):
        return f"<User {self.event_desc}>"

class eventAttendees(db.Model):
    __tablename__ = 'eventAttendees'

    user_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('eventTable.event_id'), nullable=False)
    

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f"<Event Attendee {self.user_id},{self.event_id}>"

class feedbackQuestions(db.Model):
    __tablename__ = 'feedbackQuestions'

    feedback_question_id = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback_question = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"        

class feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback_question_id = db.Column(db.Integer, db.ForeignKey('feedbackQuestions.feedback_question_id'), nullable=False)
    event_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('eventTable.event_id'), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mood = db.Column(db.Float, nullable=False)
    sentiment = db.Column(db.Float, nullable=False)

    def __init__(self, feedback_id, feedback_question_id, event_id, user_id, message, feedback_date, mood, sentiment):
        self.feedback_id = feedback_id
        self.feedback_question_id = feedback_question_id
        self.event_id = event_id
        self.user_id = user_id
        self.user_id = user_id
        self.message = message
        self.feedback_date = user_id
        self.mood = mood
        self.sentiment = sentiment

    def __repr__(self):
        return f"<Feedback {self.user_id},{self.event_id}>"
