from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateTimeField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired, EqualTo, Email



class RegistrationForm(FlaskForm):
    username = StringField('მომხმარებლის სახელი', validators=[DataRequired()])
    email = EmailField('ელ. ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    confirm_password = PasswordField('გაიმეორე პაროლი',
                                     validators=[DataRequired(), EqualTo('password',
                                     message='პაროლები არ ემთხვევა!')])
    submit = SubmitField('რეგისტრაცია')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')