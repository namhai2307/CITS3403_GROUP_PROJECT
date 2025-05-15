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
        options.add_argument("--headless=new") 
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

        return super().setUp()

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

        return super().tearDown()

    def add_test_data_to_db(self):
        """
        Add test data to the database.
        """
        user = User(username="newuser", email="newuser@example.com")
        user.set_password("Password1234")
        db.session.add(user)
        db.session.commit()

        user = User(username="queryuser", email="queryuser@example.com")
        user.set_password("Password1234")
        db.session.add(user)
        db.session.commit()

    def test_help_page_redirect(self):
        """
        Verify that the user can navigate to the help page successfully.
        """
        self.driver.get(localHost + "index")

        WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.TAG_NAME, "body")))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "help-button")))

        self.driver.find_element(By.ID, "help-button").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/help"))

        self.assertIn("/help", self.driver.current_url)
        self.assertIn("Help", self.driver.page_source)

    def test_dashboard_requires_login(self):
        """
        Verify that accessing the dashboard page without logging in redirects the user to the login page.
        """
        self.driver.get(localHost + "index")

        WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.TAG_NAME, "body")))

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "dashboard-button")))
       
        self.driver.find_element(By.ID, "dashboard-button").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))

        self.assertIn("/login", self.driver.current_url)
        self.assertIn("email", self.driver.page_source)
        self.assertIn("password", self.driver.page_source)
    
    def test_register_user(self):
        """
        Verify the user registration functionality.
        Test checks that a user can sign up/register successfully with valid credentials.
        """
        self.driver.get(localHost + "signup")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "email").send_keys("testuser@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password1234")
        self.driver.find_element(By.ID, "confirm_password").send_keys("Password1234")

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_to_be(localHost + "login"))

        self.assertIn("email", self.driver.page_source)
        self.assertIn("password", self.driver.page_source)

    def test_login_user(self):
        """
        Verify the login functionality with valid credentials.
        Using the test user created in the setup method.
        If successful, the test will check that the user is redirected to the dashboard.
        """
        self.driver.get(localHost + "login")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

        self.driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password1234")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_to_be(localHost + "dashboard"))

        self.assertEqual(self.driver.current_url, localHost + "dashboard")
        self.assertIn("Create New Event", self.driver.page_source)
        self.assertIn("My Calendar", self.driver.page_source)

    def test_logout_user(self):
        """
        Verify the logout functionality.
        Ensure that user logins in, and after clicking logout button
        They will be redirected to the home/index page after logging out.
        """
        self.driver.get(localHost + "login")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

        self.driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password1234")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/dashboard"))

        self.driver.find_element(By.LINK_TEXT, "Logout").click()

        WebDriverWait(self.driver, 10).until(EC.url_to_be(localHost + "index"))

        self.assertTrue(self.driver.current_url.endswith("/index"))
  
    
if __name__ == "__main__":
    unittest.main()
