from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.ui_utils.ui_utils import UIUtils


class CreateAccountLibs:
    """
    Page-Object for https://manage.ac2.mist.com/signin.html#!signup/register.

    """

    # Locators
    _URL = "https://manage.ac2.mist.com/signin.html#!signup/register"

    _FIRST_NAME      = (By.NAME, "firstName")
    _LAST_NAME       = (By.NAME, "lastName")
    _EMAIL           = (By.NAME, "email")
    _PASSWORD        = (By.NAME, "password")
    _COMPANY_NAME    = (By.NAME, "companyName")
    _COMPANY_ADDR1   = (By.NAME, "data-input-field")
    _COMPANY_ADDR2   = (By.NAME, "companyAddress2")
    _CITY            = (By.NAME, "city")
    _ZIP_CODE        = (By.NAME, "zipCode")
    _TERMS_CHECKBOX  = (By.CSS_SELECTOR, "input[type='checkbox']")
    _SUBMIT_BTN      = (By.CSS_SELECTOR, "button.signup-form-btn")

    # Constructor

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.ui_utils = UIUtils(driver)

    # Atomic page actions

    def navigate_to_create_account_page(self):
        """Open the Create Account page in the current browser session."""
        self.ui_utils.navigate_to(self._URL)

    def enter_first_name(self, first_name: str):
        """Type *first_name* into the First Name field."""
        self.ui_utils.send_keys(*self._FIRST_NAME, first_name)

    def enter_last_name(self, last_name: str):
        """Type *last_name* into the Last Name field."""
        self.ui_utils.send_keys(*self._LAST_NAME, last_name)

    def enter_email(self, email: str):
        """Type *email* into the Email field."""
        self.ui_utils.send_keys(*self._EMAIL, email)

    def enter_password(self, password: str):
        """Type *password* into the Password field."""
        self.ui_utils.send_keys(*self._PASSWORD, password)

    def enter_company_name(self, company_name: str):
        """Type *company_name* into the Company Name field."""
        self.ui_utils.send_keys(*self._COMPANY_NAME, company_name)

    def enter_company_address(self, address: str):
        """Type *address* into the Company Address 1 field."""
        self.ui_utils.send_keys(*self._COMPANY_ADDR1, address)

    def enter_city(self, city: str):
        """Type *city* into the City field."""
        self.ui_utils.send_keys(*self._CITY, city)

    def enter_zip_code(self, zip_code: str):
        """Type *zip_code* into the Zip Code field."""
        self.ui_utils.send_keys(*self._ZIP_CODE, zip_code)

    def accept_terms(self):
        """Check the terms-and-conditions checkbox (may be visually hidden)."""
        checkbox = self.ui_utils.find_element(*self._TERMS_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def click_create_account(self):
        """
        Scroll to and click the Create Account submit button.

        CAPTCHA may be triggered at this point; the test is considered
        complete once this click fires successfully.
        """
        self.ui_utils.scroll_to_element(*self._SUBMIT_BTN)
        self.ui_utils.click_element(*self._SUBMIT_BTN)

    # Composite workflow

    def fill_and_submit_create_account_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        company_name: str = "Test Company",
        company_address: str = "123 Test St",
        city: str = "Sunnyvale",
        zip_code: str = "94089",
    ):
        
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_company_name(company_name)
        self.enter_company_address(company_address)
        self.enter_city(city)
        self.enter_zip_code(zip_code)
        self.accept_terms()
        self.click_create_account()