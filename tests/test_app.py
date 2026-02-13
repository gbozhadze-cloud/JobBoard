import unittest
from datetime import date

from app import app, db
from models import User, Jobs
from werkzeug.security import generate_password_hash


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        user = User(
            username="testgiga",
            email="testgiga@test.com",
            password=generate_password_hash("123")
        )
        db.session.add(user)

        job = Jobs(
            title="Test Job",
            job_desc="Short desc",
            job_desc_detailed="Detailed desc",
            company="Test Company",
            salary="1000",
            location="Tbilisi",
            job_userid=1,
            author="testuser",
            date_added=date.today()
        )
        db.session.add(job)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': 'testgiga',
            'password': '123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_edit_permission_denied(self):
        response = self.client.get('/job/1/edit')
        self.assertEqual(response.status_code, 302)