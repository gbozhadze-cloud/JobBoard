from db import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_userid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    job_desc = db.Column(db.String(400), nullable=False)
    job_desc_detailed = db.Column(db.String(800), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    salary =  db.Column(db.Integer(), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=date.today)

