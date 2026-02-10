from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateTimeField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from models import *



class RegistrationForm(FlaskForm):
    username = StringField('მომხმარებლის სახელი', validators=[DataRequired()])
    email = EmailField('ელ. ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    confirm_password = PasswordField('გაიმეორე პაროლი',
                                     validators=[DataRequired(), EqualTo('password',
                                     message='პაროლები არ ემთხვევა!')])
    submit = SubmitField('რეგისტრაცია')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ეს მომხმარებლის სახელი უკვე დაკავებულია.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('ეს ელფოსტა უკვე გამოყენებულია.')




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    user = None

    def validate(self, extra_validators=None):

        user = User.query.filter_by(username=self.username.data).first()

        if not user or user.password != self.password.data:
            self.username.errors = list(self.username.errors) + ["არასწორი მომხმარებელი ან პაროლი!"]
            return False

        self.user = user
        return True



class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')