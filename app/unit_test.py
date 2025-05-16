"""
Unit tests for the Flask application.

This module contains unit tests for testing routes, models, and functionality
of the Flask application. It uses the `unittest` framework and an in-memory
SQLite database for testing.
"""

import unittest
from app import create_app, db
from app.models import User, Event
from app.config import TestConfig
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash

class PageRedirectionTests(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.

        Creates a test application using the UnitTestConfig configuration,
        initializes the application context, and sets up the in-memory
        SQLite database.
        """
        testApp = create_app(TestConfig)  
        self.app_context = testApp.app_context() 
        self.app_context.push() 
        db.create_all()  

    def tearDown(self):
        """
        Clean up after each test.

        Removes the database session, drops all tables, and pops the
        application context.
        """
        db.session.remove() 
        db.drop_all()
        self.app_context.pop() 

    def test_index_route(self):
        """
        Test the index route.

        Sends a GET request to the root URL ('/') and verifies that the
        response status code is 200 and the response contains the text
        "Who is free?".
        """
        client = create_app(TestConfig).test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Who is free?", response.data)

    def test_login_route(self):
        """
        Test the login route.

        Sends a GET request to the '/login' URL and verifies that the
        response status code is 200 and the response contains the text
        "Login".
        """
        client = create_app(TestConfig).test_client()
        response = client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.

        Creates a test application using the TestConfig configuration,
        initializes the application context, and sets up the in-memory
        SQLite database.
        """
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def add_test_data_to_db(self):
        """
        Add test data to the database.

        Creates a user and an event, associates the event with the user,
        and commits the changes to the database.
        """
        user = User(username="queryuser", email="query@example.com")
        user.set_password("QueryPassword!")
        db.session.add(user)
        db.session.commit() 

    def tearDown(self):
        """
        Clean up after each test.

        Removes the database session, drops all tables, and pops the
        application context.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insert_user(self):
        """
        Test inserting a user into the database.

        Uses add_test_data_to_db to insert a user, then queries the user
        to ensure it was inserted and has an ID assigned.
        """
        self.add_test_data_to_db()
        user = User.query.filter_by(username="queryuser").first()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)

    def test_query_user(self):
        """
        Test querying a user from the database.

        Uses add_test_data_to_db to insert a user, then queries the user
        by username to ensure it was inserted correctly.
        """
        self.add_test_data_to_db()
        queried_user = User.query.filter_by(username="queryuser").first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.email, "query@example.com")
        self.assertTrue(queried_user.check_password("QueryPassword!"))

    def test_user_password_hashing(self):
        """
        Test password hashing and verification using werkzeug's set_password.

        Creates a user, sets a password using werkzeug's set_password, and verifies that the password
        can be correctly hashed and verified with check_password.
        """
        self.add_test_data_to_db()
        user = User.query.filter_by(username="queryuser").first()
        user.set_password("QueryPassword!")
        db.session.commit()
        self.assertTrue(user.check_password("QueryPassword!"))
        self.assertFalse(user.check_password("Wrongpassword"))
        self.assertTrue(check_password_hash(user.password_hash, "QueryPassword!"))

    def test_create_event(self):
        """
        Test creating an event and associating it with a user.

        Uses add_test_data_to_db to insert a user, then creates an event,
        associates it with the user, and verifies the association.
        """
        self.add_test_data_to_db()
        user = User.query.filter_by(username="queryuser").first()

        event = Event(
            title="Test Event",
            description="This is a test event.",
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=2),
            privacy_level="private",
            user_id=user.id,
            created_by=user.id
        )
        db.session.add(event)
        db.session.commit()

        self.assertEqual(len(user.events), 1)
        self.assertEqual(user.events[0].title, "Test Event")
        self.assertEqual(user.events[0].privacy_level, "private")

    def test_event_repr(self):
        """
        Test the string representation of an event.

        Creates an event and verifies that its string representation
        matches the expected format.
        """
        event = Event(
            title="Test Event",
            description="This is a test event.",
            start_time=datetime(2025, 5, 6, 10, 0, tzinfo=timezone.utc),
            end_time=datetime(2025, 5, 6, 12, 0, tzinfo=timezone.utc),
            privacy_level="private",
            user_id=1,
            created_by=1
        )
        self.assertEqual(repr(event), "<Event Test Event (2025-05-06 10:00:00+00:00 to 2025-05-06 12:00:00+00:00)>")

if __name__ == '__main__':
    unittest.main()