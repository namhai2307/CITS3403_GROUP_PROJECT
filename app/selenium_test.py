"""
Selenium tests for the Flask application.

This module contains Selenium tests to verify the functionality of the web application,
such as navigation, form submissions, and user interactions.
"""

import unittest
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from app.config import TestConfig
from app.models import User, Event
from datetime import datetime

localHost = "http://127.0.0.1:5000/"

def run_flask_app():
    app = create_app(TestConfig)
    app.run(use_reloader=False)

class SeleniumTests(unittest.TestCase):
    """
    Selenium tests for the Flask application.
    """

    def setUp(self):
        """
        Set up the test environment and Selenium WebDriver.
        """
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.add_test_data_to_db()

        self.server_process = multiprocessing.Process(target=run_flask_app)
        self.server_process.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Run in headless mode
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        """
        Tear down the test environment and quit the WebDriver.
        """
        self.driver.quit()
        self.server_process.terminate()
        self.server_process.join()
        db.session.remove()
        db.drop_all()
        db.create_all() 
        self.app_context.pop()

    def add_test_data_to_db(self):
        """
        Add test data to the database.
        """
        existing_user = User.query.filter_by(email="newuser@example.com").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()

        user = User(username="newuser", email="newuser@example.com")
        user.set_password("Password1234")
        db.session.add(user)
        db.session.commit()

        event = Event(
            title="Test Event",
            description="This is a test event.",
            start_time=datetime(2025, 5, 8, 10, 0, 0),
            end_time=datetime(2025, 5, 8, 12, 0, 0),
            privacy_level="private",
            user_id=user.id,
            created_by=user.id
        )
        db.session.add(event)
        db.session.commit()

    def test_redirection_help(self):
        """
        Verify that the help page is accessible by user.
        Checks that user is redirected to the help page and that the page contains expected content.
        """
        self.driver.get(localHost + "help")
        self.assertEqual(self.driver.current_url, localHost + "help")
        self.assertIn("Making Your Account", self.driver.page_source)
        self.assertIn("Changing Your Details", self.driver.page_source)
        self.assertIn("Adding An Event", self.driver.page_source)

    def test_register_user(self):
        """
        Verify the user registration functionality.
        Test checks that user can signup/register successfully with credentials. 
        """
        self.driver.get(localHost + "signup")

        self.driver.find_element(By.NAME, "username").send_keys("test")
        self.driver.find_element(By.NAME, "email").send_keys("test@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("Password1234")
        self.driver.find_element(By.NAME, "confirm_password").send_keys("Password1234")

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        self.assertEqual(self.driver.current_url, localHost + "login")
        self.assertIn("email", self.driver.page_source)
        self.assertIn("password", self.driver.page_source)

    def test_login_user(self):
        """
        Verify the login functionality with valid credentials.
        Using the test user created in the setup method.
        If successful, the test will check that the user is redirected to the dashboard.
        """
        self.driver.get(localHost + "login")

        self.driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("Password1234")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_to_be(localHost + "dashboard"))

        self.assertEqual(self.driver.current_url, localHost + "dashboard")
        self.assertIn("Create New Event", self.driver.page_source)
        self.assertIn("My Calendar", self.driver.page_source)

    def test_create_event(self):
        """
        Verify the event creation functionality.
        Test proceeds to login and create a predefined event.
        If successful, the test will check that event is displayed on the dashboard.
        """
        self.driver.get(localHost + "login")
        self.driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("Password1234")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Fill out the event creation form
        self.driver.find_element(By.ID, "title").send_keys("Selenium Test Event")
        self.driver.find_element(By.ID, "description").send_keys("This is a Selenium Test Event.")
        start_time_field = self.driver.find_element(By.ID, "start_time")
        self.driver.execute_script("arguments[0].value = arguments[1];", start_time_field, "2025-05-08T10:00")
        end_time_field = self.driver.find_element(By.ID, "end_time")
        self.driver.execute_script("arguments[0].value = arguments[1];", end_time_field, "2025-05-08T12:00")
        self.driver.find_element(By.ID, "privacy_level").send_keys("private")

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the event to appear on the dashboard
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "today-events"), "Selenium Test Event")
        )

        page_text = self.driver.page_source

        self.assertIn("This is a Selenium Test Event.", page_text)
        self.assertIn("10:00 - 12:00", page_text)

    def test_logout_user(self):
        """
        Verify the logout functionality.
        Ensure that the user is redirected to the home/index page after logging out.
        """
        self.driver.get(localHost + "login")
        self.driver.find_element(By.NAME, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("Password1234")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/dashboard"))
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

        self.assertTrue(self.driver.current_url.endswith("/index"))

            
if __name__ == "__main__":
    unittest.main()

