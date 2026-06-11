# utils\ui_utils\ui_utils.py
"""UI utility functions for Selenium operations."""

import os
import shutil
import subprocess
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Config


class UIUtils:
    """Utility class for UI automation operations."""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.implicit_wait = Config.IMPLICIT_WAIT

    @staticmethod
    def get_driver() -> webdriver.Chrome:
        """
        Create and return a Chrome WebDriver instance.
        Includes multiple fallback methods for ChromeDriver setup.

        Returns:
            webdriver.Chrome: Configured Chrome driver
        """
        chrome_options = Options()

        if Config.HEADLESS:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Method 1: Try to get the correct chromedriver path
        try:
            driver_path = UIUtils._get_chromedriver_path()
            print(f"Using ChromeDriver at: {driver_path}")
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            return driver
        except Exception as e:
            print(f"Method 1 failed: {e}")

        # Method 2: Try with system ChromeDriver
        try:
            print("Trying system ChromeDriver...")
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            return driver
        except Exception as e:
            print(f"Method 2 failed: {e}")

        # Method 3: Try with Homebrew ChromeDriver
        try:
            print("Trying Homebrew ChromeDriver...")
            service = Service('/opt/homebrew/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            return driver
        except Exception as e:
            print(f"Method 3 failed: {e}")

        # Method 4: Try without specifying service (let Selenium find it)
        try:
            print("Trying default ChromeDriver...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            return driver
        except Exception as e:
            print(f"Method 4 failed: {e}")

        raise Exception("All ChromeDriver initialization methods failed. Please install ChromeDriver manually.")

    @staticmethod
    def _get_chromedriver_path():
        """
        Get the correct ChromeDriver path, fixing common issues.

        Returns:
            str: Path to ChromeDriver executable
        """
        try:
            # First, try to get the path from ChromeDriverManager
            driver_path = ChromeDriverManager().install()
            print(f"ChromeDriverManager returned: {driver_path}")

            # Check if this is actually the executable or a directory
            if os.path.isdir(driver_path):
                print("Path is a directory, looking for chromedriver executable...")
                # Look for the actual chromedriver executable in the directory
                for root, dirs, files in os.walk(driver_path):
                    for file in files:
                        if file == 'chromedriver' and os.access(os.path.join(root, file), os.X_OK):
                            actual_path = os.path.join(root, file)
                            print(f"Found executable at: {actual_path}")
                            return actual_path

            # If it's pointing to the wrong file (like THIRD_PARTY_NOTICES)
            if 'THIRD_PARTY_NOTICES' in driver_path or not driver_path.endswith('chromedriver'):
                print("Wrong file detected, looking for actual chromedriver...")
                # Get the directory and look for the real chromedriver
                driver_dir = os.path.dirname(driver_path)

                # Common patterns for chromedriver location
                possible_paths = [
                    os.path.join(driver_dir, 'chromedriver'),
                    os.path.join(os.path.dirname(driver_dir), 'chromedriver'),
                    os.path.join(driver_dir, '..', 'chromedriver'),
                ]

                for path in possible_paths:
                    if os.path.exists(path) and os.access(path, os.X_OK):
                        print(f"Found chromedriver at: {path}")
                        return path

                # If still not found, search recursively
                base_dir = os.path.dirname(driver_dir)
                for root, dirs, files in os.walk(base_dir):
                    for file in files:
                        if file == 'chromedriver':
                            full_path = os.path.join(root, file)
                            if os.access(full_path, os.X_OK):
                                print(f"Found chromedriver recursively at: {full_path}")
                                return full_path

            # If the path looks correct, verify it's executable
            if os.path.exists(driver_path) and os.access(driver_path, os.X_OK):
                return driver_path

            raise Exception(f"ChromeDriver not found or not executable at: {driver_path}")

        except Exception as e:
            print(f"Error getting ChromeDriver path: {e}")
            raise

    @staticmethod
    def install_chromedriver_manually():
        """
        Manual ChromeDriver installation guide.
        """
        print("""
        Manual ChromeDriver Installation:

        1. Download ChromeDriver from: https://chromedriver.chromium.org/
        2. Choose the version that matches your Chrome browser
        3. Extract the file and place it in one of these locations:
           - /usr/local/bin/chromedriver
           - /opt/homebrew/bin/chromedriver (for Homebrew users)
        4. Make it executable: chmod +x /path/to/chromedriver

        Or use Homebrew:
        brew install chromedriver
        """)

    def navigate_to(self, url: str):
        """Navigate to the specified URL."""
        self.driver.get(url)

    def find_element(self, by: By, value: str) -> WebElement:
        """
        Find element with explicit wait.

        Args:
            by: Locator strategy
            value: Locator value

        Returns:
            WebElement: Found element
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """
        Find multiple elements.

        Args:
            by: Locator strategy
            value: Locator value

        Returns:
            List[WebElement]: List of found elements
        """
        return self.driver.find_elements(by, value)

    def click_element(self, by: By, value: str):
        """Click element when it's clickable."""
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def send_keys(self, by: By, value: str, text: str, clear_first: bool = True):
        """
        Send keys to an element.

        Args:
            by: Locator strategy
            value: Locator value
            text: Text to send
            clear_first: Whether to clear the field first
        """
        element = self.find_element(by, value)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, by: By, value: str) -> str:
        """Get text from an element."""
        element = self.find_element(by, value)
        return element.text

    def get_attribute(self, by: By, value: str, attribute: str) -> str:
        """Get attribute value from an element."""
        element = self.find_element(by, value)
        return element.get_attribute(attribute)

    def is_element_visible(self, by: By, value: str) -> bool:
        """Check if element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except:
            return False

    def is_element_present(self, by: By, value: str) -> bool:
        """Check if element is present in DOM."""
        try:
            self.find_element(by, value)
            return True
        except:
            return False

    def wait_for_element_to_disappear(self, by: By, value: str):
        """Wait for element to disappear from DOM."""
        self.wait.until_not(EC.presence_of_element_located((by, value)))

    def wait_for_text_in_element(self, by: By, value: str, text: str):
        """Wait for specific text to appear in element."""
        self.wait.until(EC.text_to_be_present_in_element((by, value), text))

    def scroll_to_element(self, by: By, value: str):
        """Scroll to element."""
        element = self.find_element(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def select_dropdown_by_text(self, by: By, value: str, text: str):
        """Select dropdown option by visible text."""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(by, value)
        select = Select(element)
        select.select_by_visible_text(text)

    def take_screenshot(self, filename: str):
        """
        Take screenshot and save to file.

        Args:
            filename: Name of the screenshot file
        """
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def switch_to_frame(self, frame_reference):
        """Switch to iframe."""
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        """Switch back to default content from iframe."""
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str):
        """Switch to specific browser window."""
        self.driver.switch_to.window(window_handle)

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get current page title."""
        return self.driver.title

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()

    def go_back(self):
        """Navigate back in browser history."""
        self.driver.back()

    def execute_script(self, script: str, *args):
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(script, *args)