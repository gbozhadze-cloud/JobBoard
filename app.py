from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from forms import *
from models import *
from db import *



app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYSUPERSECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form=JobListForm
    joblist = Jobs.query.all()
    return render_template('index.html', form=form, joblist=joblist)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    userlist = User.query.all()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form, userlist=userlist)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect (url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')



@app.route('/add_job', methods=['GET', 'POST'])
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
        return redirect (url_for('index'))
    return render_template('add_job.html' , form=form )


@app.route("/job/<int:job_id>")
def job_details(job_id):
    job = Jobs.query.get_or_404(job_id)
    return render_template("job_details.html", job=job)

@app.route("/author/<author>")
def jobs_by_author(author):
    jobs = Jobs.query.filter_by(author=author).order_by(Jobs.date_added.desc()).all()
    return render_template("jobs_by_author.html", jobs=jobs, author=author)

@app.route("/job/<int:job_id>/edit", methods=["GET", "POST"])
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
        return redirect(url_for("job_details", job_id=job.id))

    return render_template("edit_job.html", form=form, job=job)


@app.route("/job/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    if 'username' not in session or job.author != session['username']:
        flash("თქვენ არ გაქვთ უფლებები ამ ვაკანსიის წაშლისათვის", "danger")
        return redirect(url_for("job_details", job_id=job_id))

    db.session.delete(job)
    db.session.commit()
    flash("ვაკანსია წარმატებით წაიშალა", "success")
    return redirect(url_for("index"))


@app.route('/about', methods=['GET', 'POST'])
def about ():
    return render_template('about.html')



@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}


if __name__ == '__main__':
    app.run(debug=True)

