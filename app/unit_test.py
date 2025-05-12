"""
Unit tests for the Flask application.

This module contains unit tests for testing routes, models, and functionality
of the Flask application. It uses the `unittest` framework and an in-memory
SQLite database for testing.
"""

import unittest
from app import create_app, db
from app.models import User, Event
from app.config import UnitTestConfig
from datetime import datetime, timedelta, timezone

class PageRedirectionTests(unittest.TestCase):
    """
    Test cases for basic routes in the Flask application.
    """
    def setUp(self):
        """
        Set up the test environment.

        Creates a test application using the UnitTestConfig configuration,
        initializes the application context, and sets up the in-memory
        SQLite database.
        """
        testApp = create_app(UnitTestConfig)  
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
        client = create_app(UnitTestConfig).test_client()
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
        client = create_app(UnitTestConfig).test_client()
        response = client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

class DatabaseTests(unittest.TestCase):
    """
    Test cases for models in the Flask application.
    """

    def setUp(self):
        """
        Set up the test environment.

        Creates a test application using the TestConfig configuration,
        initializes the application context, and sets up the in-memory
        SQLite database.
        """
        testApp = create_app(UnitTestConfig)
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

    def test_user_password_hashing(self):
        """
        Test password hashing and verification.

        Creates a user, sets a password, and verifies that the password
        can be correctly hashed and verified.
        """
        user = User(username="testuser", email="test@example.com")
        user.set_password("Password1234!")
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.check_password("Password1234!"))
        self.assertFalse(user.check_password("Wrongpassword"))

    def test_create_event(self):
        """
        Test creating an event and associating it with a user.

        Creates a user and an event, associates the event with the user,
        and verifies that the event is correctly linked to the user.
        """
        user = User(username="testuser", email="test@example.com")
        user.set_password("Password1234!")
        db.session.add(user)
        db.session.commit()

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
        self.assertEqual(
            repr(event),
            "<Event Test Event (2025-05-06 10:00:00+00:00 to 2025-05-06 12:00:00+00:00)>"
        )

if __name__ == '__main__':
    unittest.main()