"""
Checkout Page Object Model.
Handles all interactions with the checkout page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from pageobjects.base_page import BasePage
from utils.constants import (
    CHECKOUT_EMAIL_INPUT,
    CHECKOUT_MARKETING_CHECKBOX,
    CHECKOUT_COUNTRY_DROPDOWN,
    CHECKOUT_LAST_NAME_INPUT,
    CHECKOUT_FIRST_NAME_INPUT,
    CHECKOUT_POSTAL_CODE_INPUT,
    CHECKOUT_POSTAL_CODE_OPTIONS,
    CHECKOUT_PHONE_INPUT,
    CHECKOUT_KLARNA_LABEL,
    CHECKOUT_PAY_BUTTON
)
from utils.logger import get_logger
from utils.helpers import scroll_to_element
from config.config_manager import config

logger = get_logger()


class CheckoutPage(BasePage):
    """Page Object for Checkout page functionality."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize CheckoutPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.email_input = (By.XPATH, CHECKOUT_EMAIL_INPUT)
        self.marketing_checkbox = (By.XPATH, CHECKOUT_MARKETING_CHECKBOX)
        self.country_dropdown = (By.NAME, "countryCode")
        self.last_name_input = (By.NAME, "lastName")
        self.first_name_input = (By.NAME, "firstName")
        self.postal_code_input = (By.ID, "postalCode")
        self.postal_code_options = (By.XPATH, CHECKOUT_POSTAL_CODE_OPTIONS)
        self.phone_input = (By.NAME, "phone")
        # Using By.NAME for select element (more efficient than XPath)
        self.phone_country_dropdown = (By.NAME, "phone_country_select")
        self.klarna_label = (By.XPATH, CHECKOUT_KLARNA_LABEL)
        self.pay_button = (By.ID, "checkout-pay-button")
    
    def enter_email(self, email: str):
        """
        Enter email address.
        
        Args:
            email: Email address
        """
        logger.info(f"Entering email: {email}")
        self.send_keys(self.email_input, email)
    
    def check_marketing_opt_in(self):
        """Check the marketing opt-in checkbox."""
        logger.info("Checking marketing opt-in checkbox")
        if not self.is_element_visible(self.marketing_checkbox, timeout=2):
            logger.warning("Marketing checkbox not found, skipping")
            return
        checkbox = self.wait_utils.wait_for_element_clickable(self.marketing_checkbox)
        if not checkbox.is_selected():
            checkbox.click()
    
    def select_country(self, country_name: str):
        """
        Select country from dropdown.
        
        Args:
            country_name: Country name to select (e.g., "Japan", "United States")
        """
        logger.info(f"Selecting country: {country_name}")
        country_select = Select(self.wait_utils.wait_for_element_visible(self.country_dropdown))
        try:
            country_select.select_by_visible_text(country_name)
            logger.info(f"Successfully selected country: {country_name}")
        except NoSuchElementException:
            logger.error(f"Country '{country_name}' not found in dropdown")
            raise
    
    def enter_last_name(self, last_name: str):
        """
        Enter last name.
        
        Args:
            last_name: Last name
        """
        logger.info(f"Entering last name: {last_name}")
        self.send_keys(self.last_name_input, last_name)
    
    def enter_first_name(self, first_name: str):
        """
        Enter first name.
        
        Args:
            first_name: First name
        """
        logger.info(f"Entering first name: {first_name}")
        self.send_keys(self.first_name_input, first_name)
    
    def enter_postal_code(self, postal_code: str):
        """
        Enter postal code.
        
        Args:
            postal_code: Postal code
        """
        logger.info(f"Entering postal code: {postal_code}")
        self.send_keys(self.postal_code_input, postal_code)
    
    def select_postal_code_option(self, search_text: str = "Iguchi"):
        """
        Select postal code option from autocomplete dropdown.
        
        Args:
            search_text: Text to search for in options (default: "Iguchi")
        
        Returns:
            True if option selected, False otherwise
        """
        logger.info(f"Selecting postal code option containing: {search_text}")
        try:
            options = self.wait_utils.wait_for_elements_present(
                self.postal_code_options,
                min_count=1,
                timeout=config.short_timeout
            )
            logger.debug(f"Found {len(options)} postal code options")
            
            for option in options:
                option_text = option.text
                logger.debug(f"Checking option: {option_text}")
                if search_text in option_text:
                    logger.info(f"Selecting postal code option: {option_text}")
                    option.click()
                    return True
            
            logger.warning(f"No postal code option found containing '{search_text}'")
            return False
        except Exception as e:
            logger.warning(f"Failed to select postal code option: {e}")
            return False
    
    def enter_phone(self, phone: str):
        """
        Enter phone number.
        
        Args:
            phone: Phone number
        """
        logger.info(f"Entering phone: {phone}")
        self.send_keys(self.phone_input, phone)
    
    def select_phone_country_code(self, country_code: str):
        """
        Select phone country code from dropdown.
        
        Args:
            country_code: Country code value (e.g., "IN", "US", "JP")
        """
        logger.info(f"Selecting phone country code: {country_code}")
        try:
            # Wait for dropdown to be present (don't need it to be visible for Select)
            dropdown = self.wait_utils.wait_for_element_present(self.phone_country_dropdown)
            
            # Scroll element into view to ensure it's accessible
            scroll_to_element(self.driver, dropdown)
            
            # For standard HTML select elements, Select() works without clicking
            # Try Select directly first (this is the standard and most reliable approach)
            country_code_select = Select(dropdown)
            logger.debug(f"Total country code options: {len(country_code_select.options)}")
            
            # Select by value
            country_code_select.select_by_value(country_code)
            logger.info(f"Successfully selected phone country code: {country_code}")
            
        except Exception as e:
            logger.error(f"Failed to select phone country code '{country_code}': {e}")
            # If Select fails, it might be a custom dropdown - log for debugging
            logger.debug("If this is a custom dropdown, may need special handling")
            raise
    
    def fill_checkout_form(
        self,
        email: str,
        last_name: str,
        first_name: str,
        postal_code: str,
        phone: str,
        phone_country_code: str,
        country: str = "Japan",
        postal_search_text: str = "Iguchi"
    ):
        """
        Fill complete checkout form.
        
        Args:
            email: Email address
            last_name: Last name
            first_name: First name
            postal_code: Postal code
            phone: Phone number
            phone_country_code: Phone country code (e.g., "IN")
            country: Country name (default: "Japan")
            postal_search_text: Text to search in postal code options (default: "Iguchi")
        """
        logger.info("Filling checkout form")
        self.enter_email(email)
        self.check_marketing_opt_in()
        self.select_country(country)
        self.enter_last_name(last_name)
        self.enter_first_name(first_name)
        self.enter_postal_code(postal_code)
        self.select_postal_code_option(postal_search_text)
        self.enter_phone(phone)
        self.select_phone_country_code(phone_country_code)
        logger.info("Checkout form filled successfully")
    
    def select_klarna_payment(self):
        """Select Klarna as payment method."""
        logger.info("Selecting Klarna payment method")
        try:
            klarna_label_element = self.wait_utils.wait_for_element_visible(self.klarna_label)
            scroll_to_element(self.driver, klarna_label_element)
            
            # Use JavaScript click in case element is not directly clickable
            self.driver.execute_script("arguments[0].click();", klarna_label_element)
            logger.info("Successfully selected Klarna payment method")
        except Exception as e:
            logger.error(f"Failed to select Klarna payment: {e}")
            raise
    
    def click_pay_button(self):
        """Click the pay/checkout button."""
        logger.info("Clicking pay button")
        try:
            pay_button_element = self.wait_utils.wait_for_element_present(self.pay_button)
            
            # Scroll to button
            scroll_to_element(self.driver, pay_button_element)
            
            # Wait for button to be clickable and click
            self.wait_utils.wait_for_element_clickable(self.pay_button).click()
            logger.info("Successfully clicked pay button")
        except Exception as e:
            logger.error(f"Failed to click pay button: {e}")
            raise
    
    def complete_checkout_with_klarna(self):
        """Complete checkout by selecting Klarna and clicking pay button."""
        logger.info("Completing checkout with Klarna")
        self.select_klarna_payment()
        self.click_pay_button()
