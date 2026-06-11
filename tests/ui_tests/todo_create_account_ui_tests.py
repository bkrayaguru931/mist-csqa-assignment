import time
import pytest
import logging
from datetime import datetime

from libs.ui_libs.todo_create_account_libs import CreateAccountLibs
from utils.ui_utils.ui_utils import UIUtils

class TestCreateAccount:
    """
    The test navigates to the signup page, populates all required fields
    with generated data, and clicks the Create Account button.  If CAPTCHA
    is triggered after the click, that is acceptable — the assignment
    requirement is only that the button is successfully clicked.
    """

    # Fixtures

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Method-scoped fixture: spin up a fresh WebDriver before each test
        and quit it unconditionally afterward.
        """
        self.driver = UIUtils.get_driver()
        self.create_account = CreateAccountLibs(self.driver)
        yield
        self.driver.quit()

    # Test case
    

    def test_create_account(self):
        """
        Fill in the Create Account form and click Submit.

        Steps
        -----
        1. Navigate to https://manage.ac2.mist.com/signin.html#!signup/register
        2. Assert the browser actually landed on the signup page.
        3. Enter generated test data into every required field.
        4. Click the Create Account button.
           (CAPTCHA may appear — the test ends here regardless.)
        """
        logging.info("*" * 89)
        logging.info("###  test_create_account  ###")

        #  Step 1: navigate 
        self.create_account.navigate_to_create_account_page()

        # Brief wait to render the signup fragment.
        self.create_account.wait_for_page_load()

        #  Step 2: verify URL 
        current_url = self.driver.current_url
        assert "signup/register" in current_url, (
            f"Expected signup/register page, but landed on: {current_url}"
        )
        logging.info("Confirmed signup/register page loaded: %s", current_url)

        #  Step 3: build unique test data 
        # Using a millisecond-precision timestamp avoids duplicate-email
        # rejections on repeated test runs.
        timestamp = str(int(datetime.now().timestamp() * 1000))
        first_name = "AutoFirst"
        last_name  = "AutoLast"
        email      = f"autouser_{timestamp}@testautomation.example"
        password   = "TestPassword@123"

        logging.info("Test data → email: %s", email)

        #  Step 4: fill form and click
        self.create_account.fill_and_submit_create_account_form(
            first_name, last_name, email, password
        )

        logging.info("Create Account button clicked — test complete.")
        # CAPTCHA or next-step navigation may follow; both are acceptable
        # outcomes per the assignment specification.