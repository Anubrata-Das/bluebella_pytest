"""
Wait utilities for Selenium WebDriver.
Provides custom wait conditions and helper methods.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from config.config_manager import config
from utils.logger import get_logger

logger = get_logger()


class WaitUtils:
    """Utility class for WebDriver wait operations."""
    
    def __init__(self, driver, timeout=None):
        """
        Initialize WaitUtils.
        
        Args:
            driver: WebDriver instance
            timeout: Wait timeout in seconds (defaults to config value)
        """
        self.driver = driver
        self.timeout = timeout or config.default_timeout
        self.wait = WebDriverWait(driver, self.timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        
        Returns:
            WebElement if found
        
        Raises:
            TimeoutException if element not visible within timeout
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {timeout or self.timeout}s: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        
        Returns:
            WebElement if found
        
        Raises:
            TimeoutException if element not clickable within timeout
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout or self.timeout}s: {locator}")
            raise
    
    def wait_for_element_present(self, locator, timeout=None):
        """
        Wait for element to be present in DOM.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        
        Returns:
            WebElement if found
        
        Raises:
            TimeoutException if element not present within timeout
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element present: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not present within {timeout or self.timeout}s: {locator}")
            raise
    
    def wait_for_elements_present(self, locator, timeout=None, min_count=1):
        """
        Wait for multiple elements to be present.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
            min_count: Minimum number of elements expected
        
        Returns:
            List of WebElements
        
        Raises:
            TimeoutException if not enough elements found
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            elements = wait.until(lambda driver: driver.find_elements(*locator))
            if len(elements) >= min_count:
                logger.debug(f"Found {len(elements)} elements: {locator}")
                return elements
            else:
                raise TimeoutException(f"Only found {len(elements)} elements, expected at least {min_count}")
        except TimeoutException:
            logger.error(f"Not enough elements found within {timeout or self.timeout}s: {locator}")
            raise
    
    def wait_for_url_contains(self, text, timeout=None):
        """
        Wait for URL to contain specified text.
        
        Args:
            text: Text to search in URL
            timeout: Optional timeout override
        
        Returns:
            True if URL contains text
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            result = wait.until(EC.url_contains(text))
            logger.debug(f"URL contains '{text}': {self.driver.current_url}")
            return result
        except TimeoutException:
            logger.error(f"URL does not contain '{text}' within {timeout or self.timeout}s")
            raise
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """
        Wait for element to contain specified text.
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to wait for
            timeout: Optional timeout override
        
        Returns:
            WebElement if text found
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            element = wait.until(EC.text_to_be_present_in_element(locator, text))
            logger.debug(f"Text '{text}' found in element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Text '{text}' not found in element within {timeout or self.timeout}s: {locator}")
            raise
    
    def is_element_visible(self, locator, timeout=2):
        """
        Check if element is visible without raising exception.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Short timeout for quick check
        
        Returns:
            True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=2):
        """
        Check if element is present without raising exception.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Short timeout for quick check
        
        Returns:
            True if present, False otherwise
        """
        try:
            self.wait_for_element_present(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

