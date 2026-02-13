import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from forms import *
from models import *
from db import *
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYSUPERSECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = "static/images"

db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(filename='logs/myapp.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_required(f):  #ამ დეკორატორს აქ გადაეცემა ჩვენი როუტის ფუნციები შემდეგში
    @wraps(f)           # ეს შეუნახავს ორიგინალ ფუნქციის სახელებს ფლასკს
    def wrapper(*args, **kwargs): # wrapper ით ჩანაცვლდება თუ დალოგინებული არ არის , იღებს ნებისმიერ პარამეტრებს
        if "user_id" not in session:
            flash("გთხოვთ შესვლა განახორციელოთ", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route('/', methods=['GET', 'POST'])
def index():

    form=JobListForm()
    joblist = Jobs.query.all()
    # ვალუტის კურსები
    try:
        url = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json"
        response = requests.get(url)
        valutis_kursebi = []
        data = response.json()
        valutis_kursebi = [val for val in data[0]["currencies"] if val["code"] in ("USD", "EUR")]
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
    return render_template('index.html', form=form, joblist=joblist,valutis_kursebi=valutis_kursebi)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    userlist = User.query.all()
    if form.validate_on_submit():
        existing_user = User.query.filter(             #შემოწმება თ არის უკვე მომხმარებელი ან ფოსტა
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash("მომხმარებელი ან email უკვე არსებობს!", "danger")
            return render_template('register.html', form=form, userlist=userlist)

        #აქ დავჰეშავთ პაროლს
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=16
        )

        user = User(username=form.username.data,
                    password=hashed_password,
                    email=form.email.data
                    )
        db.session.add(user)
        db.session.commit()
        flash("რეგისტრაცია წარმატებულია!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, userlist=userlist)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data or ""
        password = form.password.data or ""
        user = User.query.filter_by(username=username).first() if username else None


        if form.validate_on_submit() and user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"მოგესალმები {user.username}!", "success")
            logging.info(f"SUCCESSFUL login: username={user.username}")
            return redirect(url_for('index'))
        else:
            flash("არასწორი მომხმარებელი ან პაროლი!", "danger")
            logging.warning(f"FAILED login attempt: username={username}")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        # სურათის ატვირთვა
        if form.profile_pic.data:
            image_file = form.profile_pic.data
            filename = image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
            user.profile_pic = filename

        db.session.commit()
        session['username'] = user.username
        flash("პროფილი განახლდა!", "success")
        return redirect(url_for('profile'))


    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email

    return render_template('profile.html', form=form, user=user)



@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        new_job = Jobs(
            title = form.title.data,
            job_userid = session["user_id"],
            author = session["username"],
            job_desc = form.job_desc.data,
            job_desc_detailed = form.job_desc_detailed.data,
            company = form.company.data,
            salary=form.salary.data,
            location=form.location.data
        )
        db.session.add(new_job)
        db.session.commit()
        logging.info(f"SUCCESSFUL Added job: username={session["username"]}")
        return redirect (url_for('index'))
    return render_template('add_job.html' , form=form )


@app.route("/job/<int:job_id>")
def job_details(job_id):
    job = Jobs.query.get_or_404(job_id)
    return render_template("job_details.html", job=job)

@app.route("/author/<author>")
@login_required
def jobs_by_author(author):
    jobs = Jobs.query.filter_by(author=author).order_by(Jobs.date_added.desc()).all()
    return render_template("jobs_by_author.html", jobs=jobs, author=author)

@app.route("/job/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    job = Jobs.query.get_or_404(job_id)
    if 'username' not in session or job.author != session['username']:
        flash("თქვენ არ გაქვთ უფლებები ამ ვაკანსიის რედაქტირებისათვის", "danger")
        return redirect(url_for("job_details", job_id=job_id))

    form = JobForm(obj=job)  # pre-fill with existing job info
    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.salary = form.salary.data
        job.job_desc = form.job_desc.data
        job.job_desc_detailed = form.job_desc_detailed.data
        db.session.commit()
        flash("ვაკანსია წარმატებით განახლდა", "success")
        logging.info(f"SUCCESSFUL Edited job: username={session["username"]}")
        return redirect(url_for("job_details", job_id=job.id))

    return render_template("edit_job.html", form=form, job=job)


@app.route("/job/<int:job_id>/delete", methods=["POST"])
@login_required
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    if 'username' not in session or job.author != session['username']:
        flash("თქვენ არ გაქვთ უფლებები ამ ვაკანსიის წაშლისათვის", "danger")
        return redirect(url_for("job_details", job_id=job_id))

    db.session.delete(job)
    db.session.commit()
    logging.info(f"SUCCESSFUL Deleted job: username={session["username"]}")
    flash("ვაკანსია წარმატებით წაიშალა", "success")
    return redirect(url_for("index"))


@app.route('/about', methods=['GET', 'POST'])
def about ():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}


if __name__ == '__main__':
    app.run(debug=True)

