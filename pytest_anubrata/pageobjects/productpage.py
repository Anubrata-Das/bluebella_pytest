"""
Product Page Object Model.
Handles all interactions with the product detail page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pageobjects.base_page import BasePage
from utils.constants import (
    ADD_TO_CART_BUTTON,
    CART_DRAWER_CLOSE_BUTTON,
    QUICK_ADD_TO_CART_BUTTON,
    CHECKOUT_BUTTON,
    COMPLETE_THE_LOOK_SECTION,
    COMPLETE_THE_LOOK_ITEMS,
    SIZE_OPTION_CLASS
)
from utils.logger import get_logger
from utils.helpers import scroll_to_element
from config.config_manager import config

logger = get_logger()


class ProductPage(BasePage):
    """Page Object for Product Detail page functionality."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize ProductPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.add_to_cart_button = (By.XPATH, ADD_TO_CART_BUTTON)
        self.cart_drawer_close_button = (By.XPATH, CART_DRAWER_CLOSE_BUTTON)
        self.quick_add_to_cart_button = (By.XPATH, QUICK_ADD_TO_CART_BUTTON)
        self.checkout_button = (By.XPATH, CHECKOUT_BUTTON)
        self.complete_the_look_section = (By.XPATH, COMPLETE_THE_LOOK_SECTION)
        self.complete_the_look_items = (By.XPATH, COMPLETE_THE_LOOK_ITEMS)
    
    def select_size_if_available(self, size_text: str) -> bool:
        """
        Select size option if available.
        
        Args:
            size_text: Size to select (e.g., "38", "D", "M")
        
        Returns:
            True if size was selected, False if not available
        """
        logger.info(f"Attempting to select size: {size_text}")
        size_locator = (
            By.XPATH,
            f"//div[contains(@class,'{SIZE_OPTION_CLASS}')][normalize-space(text())='{size_text}']"
        )
        
        if self.is_element_visible(size_locator, timeout=3):
            try:
                self.click_element(size_locator)
                logger.info(f"Successfully selected size: {size_text}")
                return True
            except Exception as e:
                logger.warning(f"Size '{size_text}' visible but not clickable: {e}")
                return False
        else:
            logger.debug(f"Size '{size_text}' not available")
            return False
    
    def add_to_cart(self):
        """Click the add to cart button."""
        logger.info("Adding product to cart")
        self.click_element(self.add_to_cart_button)
        # Wait for cart drawer to appear
        self.wait_utils.wait_for_element_visible(self.cart_drawer_close_button)
    
    def close_cart_drawer(self):
        """Close the cart drawer."""
        logger.info("Closing cart drawer")
        if self.is_element_visible(self.cart_drawer_close_button, timeout=3):
            self.click_element(self.cart_drawer_close_button)
            # Wait for drawer to close (checking it's no longer visible)
            # Using a short timeout to verify drawer closed
            try:
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.common.exceptions import TimeoutException
                WebDriverWait(self.driver, config.short_timeout).until(
                    EC.invisibility_of_element_located((By.XPATH, "//div[@class='cart-drawer']"))
                )
            except TimeoutException:
                logger.debug("Cart drawer may still be visible")
            logger.debug("Cart drawer closed")
    
    def add_to_cart_and_close_drawer(self):
        """
        Add item to cart and close the drawer.
        Common workflow for adding items to cart.
        """
        logger.info("Adding to cart and closing drawer")
        self.add_to_cart()
        self.close_cart_drawer()
    
    def scroll_to_complete_the_look_section(self):
        """Scroll to the 'Complete the Look' carousel section."""
        logger.info("Scrolling to 'Complete the Look' section")
        try:
            carousel_element = self.wait_utils.wait_for_element_present(
                self.complete_the_look_section
            )
            scroll_to_element(self.driver, carousel_element)
            logger.debug("Scrolled to Complete the Look section")
        except TimeoutException:
            logger.warning("Complete the Look section not found on page")
            raise
    
    def get_complete_the_look_items(self):
        """
        Get all items from the Complete the Look carousel.
        
        Returns:
            List of WebElements representing carousel items
        """
        logger.debug("Getting Complete the Look items")
        items = self.wait_utils.wait_for_elements_present(
            self.complete_the_look_items,
            min_count=1
        )
        logger.debug(f"Found {len(items)} items in Complete the Look")
        return items
    
    def click_last_complete_the_look_item(self):
        """
        Click the last item in the Complete the Look carousel.
        
        Raises:
            NoSuchElementException: If no items found or cannot click
        """
        logger.info("Clicking last item in Complete the Look")
        
        self.scroll_to_complete_the_look_section()
        
        items = self.get_complete_the_look_items()
        
        if not items:
            raise NoSuchElementException("No items found in Complete the Look section")
        
        # Get the last item
        last_item = items[-1]
        logger.debug(f"Found {len(items)} items, selecting last one")
        
        # Scroll last item into view
        scroll_to_element(self.driver, last_item)
        
        # Find and click the add button within the last item
        try:
            add_button = last_item.find_element(
                By.XPATH,
                ".//div[contains(@class,'product-card__details')]//button"
            )
            self.wait_utils.wait_for_element_clickable(
                (By.XPATH, ".//div[contains(@class,'product-card__details')]//button"),
                timeout=config.short_timeout
            )
            add_button.click()
            logger.info("Successfully clicked last Complete the Look item")
        except Exception as e:
            logger.error(f"Failed to click last item: {e}")
            raise
    
    def select_quick_add_size_if_available(self, size_text: str) -> bool:
        """
        Select size in quick add section if available.
        
        Args:
            size_text: Size to select
        
        Returns:
            True if size was selected, False otherwise
        """
        logger.info(f"Attempting to select quick add size: {size_text}")
        size_locator = (
            By.XPATH,
            f"//div[@class='product-quick-add__container']//div[contains(@class,'{SIZE_OPTION_CLASS}')][normalize-space(text())='{size_text}']"
        )
        
        if self.is_element_visible(size_locator, timeout=3):
            try:
                self.click_element(size_locator)
                logger.info(f"Successfully selected quick add size: {size_text}")
                return True
            except Exception as e:
                logger.warning(f"Quick add size '{size_text}' visible but not clickable: {e}")
                return False
        else:
            logger.debug(f"Quick add size '{size_text}' not available")
            return False
    
    def click_quick_add_to_cart(self):
        """Click the quick add to cart button."""
        logger.info("Clicking quick add to cart button")
        self.click_element(self.quick_add_to_cart_button)
        # Wait for cart drawer to appear
        self.wait_utils.wait_for_element_visible(self.checkout_button, timeout=config.long_timeout)
    
    def click_checkout_button(self):
        """Click the checkout button in cart drawer."""
        logger.info("Clicking checkout button")
        self.click_element(self.checkout_button)
    
    def proceed_to_checkout(self):
        """
        Complete workflow: quick add to cart and proceed to checkout.
        """
        logger.info("Proceeding to checkout")
        self.click_quick_add_to_cart()
        self.click_checkout_button()
