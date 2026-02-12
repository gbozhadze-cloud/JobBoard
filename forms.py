from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateTimeField, IntegerField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
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



class AddJobForm(FlaskForm):
    title = StringField('ვაკანსიის დასახელება', validators=[DataRequired(), Length(max=200)])
    job_desc = StringField('ვაკანსიის აღწერა', validators=[DataRequired(), Length(max=400)])
    job_desc_detailed = TextAreaField("დეტალური აღწერა", validators=[DataRequired(), Length(max=800)])
    company = StringField('კომპანიის დასახელება', validators=[DataRequired(), Length(max=200)])
    salary = IntegerField('განსაზღვრული ხელფასი', validators=[DataRequired()])
    location = StringField('ლოკაცია', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Post')

class JobListForm(FlaskForm):
    id = StringField('id')
    title = StringField('ვაკანსიის დასახელება')
    job_desc = StringField('ვაკანსიის აღწერა')
    job_desc_detailed = TextAreaField("დეტალური აღწერა")
    company = StringField('კომპანიის დასახელება')
    salary = StringField('განსაზღვრული ხელფასი')
    location = StringField('ლოკაცია')
    author = StringField('ავტორი')

class JobForm(FlaskForm):
    title = StringField('ვაკანსიის დასახელება', validators=[DataRequired(), Length(max=200)])
    company = StringField('კომპანიის დასახელება', validators=[DataRequired(), Length(max=200)])
    location = StringField('ლოკაცია', validators=[DataRequired(), Length(max=200)])
    salary = StringField('განსაზღვრული ხელფასი', validators=[DataRequired()])
    job_desc = TextAreaField('ვაკანსიის აღწერა', validators=[DataRequired(), Length(max=400)])
    job_desc_detailed = TextAreaField('დეტალური აღწერა', validators=[DataRequired(), Length(max=800)])
    submit = SubmitField('Post')