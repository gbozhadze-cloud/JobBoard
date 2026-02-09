from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateTimeField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired


class AddStudent(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    course = StringField('Course Name', validators=[DataRequired()])
    value = IntegerField('Value', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    sumbit = SubmitField('Submit')

class StudentListForm(FlaskForm):
    pass


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')