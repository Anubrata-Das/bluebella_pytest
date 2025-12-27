"""
Base Page Object class.
All page objects should inherit from this class for common functionality.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from config.config_manager import config
from utils.waits import WaitUtils
from utils.logger import get_logger
from utils.helpers import wait_for_page_load

logger = get_logger()


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize base page.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait_utils = WaitUtils(driver, config.default_timeout)
        self.wait = WebDriverWait(driver, config.default_timeout)
    
    def get_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title string
        """
        title = self.driver.title
        logger.debug(f"Page title: {title}")
        return title
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL string
        """
        url = self.driver.current_url
        logger.debug(f"Current URL: {url}")
        return url
    
    def navigate_to(self, url: str):
        """
        Navigate to specified URL.
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        wait_for_page_load(self.driver)
    
    def refresh_page(self):
        """Refresh the current page."""
        logger.debug("Refreshing page")
        self.driver.refresh()
        wait_for_page_load(self.driver)
    
    def click_element(self, locator: tuple, timeout: int = None):
        """
        Click an element with explicit wait.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        """
        element = self.wait_utils.wait_for_element_clickable(locator, timeout)
        element.click()
        logger.debug(f"Clicked element: {locator}")
    
    def send_keys(self, locator: tuple, text: str, timeout: int = None):
        """
        Send keys to an element with explicit wait.
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to send
            timeout: Optional timeout override
        """
        element = self.wait_utils.wait_for_element_visible(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.debug(f"Sent keys to element: {locator}")
    
    def get_element_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        
        Returns:
            Element text
        """
        element = self.wait_utils.wait_for_element_visible(locator, timeout)
        text = element.text
        logger.debug(f"Got text from element {locator}: {text}")
        return text
    
    def is_element_visible(self, locator: tuple, timeout: int = 2) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Short timeout for quick check
        
        Returns:
            True if visible, False otherwise
        """
        return self.wait_utils.is_element_visible(locator, timeout)
    
    def scroll_to_element(self, locator: tuple, timeout: int = None):
        """
        Scroll to element using JavaScript.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional timeout override
        """
        from utils.helpers import scroll_to_element
        element = self.wait_utils.wait_for_element_present(locator, timeout)
        scroll_to_element(self.driver, element)
        logger.debug(f"Scrolled to element: {locator}")

