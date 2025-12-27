"""
Login Page Object Model.
Handles all interactions with the login page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pageobjects.base_page import BasePage
from utils.constants import (
    LOGIN_HEADER_BUTTON,
    LOGIN_EMAIL_INPUT,
    LOGIN_PASSWORD_INPUT,
    LOGIN_SIGNIN_BUTTON
)
from utils.logger import get_logger

logger = get_logger()


class LoginPage(BasePage):
    """Page Object for Login functionality."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize LoginPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.header_button = (By.XPATH, LOGIN_HEADER_BUTTON)
        self.email_input = (By.XPATH, LOGIN_EMAIL_INPUT)
        self.password_input = (By.XPATH, LOGIN_PASSWORD_INPUT)
        self.signin_button = (By.XPATH, LOGIN_SIGNIN_BUTTON)
    
    def click_account_icon(self):
        """Click the account icon to open login form."""
        logger.info("Clicking account icon")
        self.click_element(self.header_button)
    
    def enter_email(self, email: str):
        """
        Enter email address.
        
        Args:
            email: Email address to enter
        """
        logger.info(f"Entering email: {email}")
        self.send_keys(self.email_input, email)
    
    def enter_password(self, password: str):
        """
        Enter password.
        
        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.send_keys(self.password_input, password)
    
    def click_signin_button(self):
        """Click the sign in button."""
        logger.info("Clicking sign in button")
        self.click_element(self.signin_button)
    
    def login(self, username: str, password: str):
        """
        Perform complete login flow.
        
        Args:
            username: User email address
            password: User password
        """
        logger.info(f"Logging in user: {username}")
        self.click_account_icon()
        self.enter_email(username)
        self.enter_password(password)
        self.click_signin_button()
    
    def is_signed_in(self) -> bool:
        """
        Check if user is signed in by checking URL.
        
        Returns:
            True if on account page, False otherwise
        """
        current_url = self.get_current_url()
        is_signed_in = current_url.startswith("https://www.bluebella.com/account")
        logger.info(f"User signed in: {is_signed_in}")
        return is_signed_in
    
    def navigate_back_to_homepage(self, original_url: str):
        """
        Navigate back to homepage after login.
        
        Args:
            original_url: URL to navigate back to
        """
        if self.is_signed_in():
            logger.info(f"Navigating back to: {original_url}")
            self.navigate_to(original_url)
        else:
            logger.warning("User not signed in, skipping navigation")