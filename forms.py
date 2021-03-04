from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, DateField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.simple import HiddenField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SessionCreationForm(FlaskForm):
    session_name = StringField('Session Name', validators=[DataRequired(), Length(min=3, max=30)])
    # session_type = RadioField('Session Type', choices=[(1, 'Seminar'),(2, 'Workshop'),(3, 'Presentation')],validators=[DataRequired()] )
    session_type = StringField('Session Type', validators=[DataRequired(), Length(min=3, max=30)]) 
    session_start = DateField('Session Start', format='%m/%d/%Y',validators=[DataRequired()])
    session_end = DateField('Session End', format='%m/%d/%Y',validators=[DataRequired()])
    submit = SubmitField('Create Session')
    
class SessionJoinForm(FlaskForm):
    session_code = StringField('Session Code',validators=[DataRequired()]) 
    submit = SubmitField('Join Session')

class SessionQuestion(FlaskForm):
    question_id = HiddenField()
    # TODO: GET QUESTION NAME 
    question = StringField(validators=[DataRequired()])

class AttendeeForm(FlaskForm):
    feedback_questions = FieldList(FormField(SessionQuestion))
    mood_type = RadioField('Mood', choices=[(1, ':D'),(2, ':I'),(3, ':(')],validators=[DataRequired()] )
    submit = SubmitField('Submit Feedback')

class HostForm(FlaskForm):
    add_feedback_question = StringField('Add Question', validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')