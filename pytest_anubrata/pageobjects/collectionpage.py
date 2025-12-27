"""
Collection Page Object Model.
Handles all interactions with the product collection page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pageobjects.base_page import BasePage
from utils.constants import (
    PRODUCT_GRID_ITEMS,
    SORT_BY_BUTTON,
    PRODUCT_TITLE_CLASS
)
from utils.logger import get_logger
from utils.helpers import scroll_to_element
from config.config_manager import config

logger = get_logger()


class CollectionPage(BasePage):
    """Page Object for Product Collection page functionality."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize CollectionPage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.product_grid_items = (By.XPATH, PRODUCT_GRID_ITEMS)
        self.sort_by_button = (By.CSS_SELECTOR, SORT_BY_BUTTON)
    
    def click_sort_by_button(self):
        """Click the sort by dropdown button."""
        logger.info("Clicking sort by button")
        self.click_element(self.sort_by_button)
    
    def select_sort_option(self, sort_option: str):
        """
        Select sorting option from dropdown.
        
        Args:
            sort_option: Text of the sort option to select (e.g., "Newest", "Price: Low to High")
        """
        logger.info(f"Selecting sort option: {sort_option}")
        sort_option_locator = (
            By.XPATH,
            f"(//div[contains(@class,'collection-filter__sorting')]//button[contains(normalize-space(.),'{sort_option}')])[1]"
        )
        self.click_element(sort_option_locator)
    
    def sort_by_text(self, sort_text: str):
        """
        Complete sort operation by text.
        
        Args:
            sort_text: Sorting option text
        """
        logger.info(f"Sorting products by: {sort_text}")
        self.click_sort_by_button()
        self.wait_utils.wait_for_element_clickable(
            (By.XPATH, "//div[contains(@class,'collection-filter__sorting')]//button"),
            timeout=config.short_timeout
        )
        self.select_sort_option(sort_text)
        # Wait for products to reload after sorting
        self.wait_utils.wait_for_elements_present(self.product_grid_items, min_count=1)
    
    def scroll_full_collection_page(self, max_scrolls: int = 50):
        """
        Scroll down until no more products are loaded (lazy loading).
        
        Args:
            max_scrolls: Maximum number of scroll attempts to prevent infinite loops
        """
        logger.info("Scrolling collection page to load all products")
        last_height = 0
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for potential lazy-loaded content
            self.wait_utils.wait_for_element_present(
                self.product_grid_items,
                timeout=config.short_timeout
            )
            
            # Check if page height changed
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logger.debug(f"Reached bottom after {scroll_count} scrolls")
                break
            
            last_height = new_height
            scroll_count += 1
        
        if scroll_count >= max_scrolls:
            logger.warning(f"Reached maximum scroll limit: {max_scrolls}")
    
    def find_product_by_name(self, product_name: str):
        """
        Find product element by name using incremental scrolling for lazy-loaded content.
        Scrolls 400px at a time and checks if product is visible in viewport.
        
        Args:
            product_name: Exact product name to find
        
        Returns:
            WebElement if found
        
        Raises:
            NoSuchElementException: If product not found
        """
        logger.info(f"Searching for product: {product_name} using incremental scrolling")
        
        scroll_amount = 400  # pixels to scroll at a time
        max_scrolls = 100  # Maximum number of scrolls to prevent infinite loop
        scroll_position = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        for scroll_count in range(max_scrolls):
            # Get all currently loaded product elements
            products = self.driver.find_elements(*self.product_grid_items)
            
            if not products:
                logger.warning("No products found on page yet")
                # Scroll a bit to trigger lazy loading
                scroll_position += scroll_amount
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                self.wait_utils.wait_for_element_present(
                    self.product_grid_items,
                    timeout=config.short_timeout
                )
                continue
            
            logger.debug(f"Checking {len(products)} products after scroll {scroll_count + 1}")
            
            # Check each product to see if it matches and is visible
            for idx, product in enumerate(products):
                try:
                    # Get product title
                    title_element = product.find_element(
                        By.XPATH,
                        f".//*[contains(@class,'{PRODUCT_TITLE_CLASS}')]"
                    )
                    title_text = title_element.text.strip()
                    
                    # If product name matches, scroll to it and return
                    if title_text == product_name:
                        logger.info(f"Found matching product '{product_name}'")
                        # Scroll product into view to ensure it's fully loaded
                        scroll_to_element(self.driver, product)
                        # Wait a moment for any lazy-loaded images/content
                        self.wait_utils.wait_for_element_present(
                            (By.XPATH, f".//*[contains(@class,'{PRODUCT_TITLE_CLASS}')]"),
                            timeout=config.short_timeout
                        )
                        return product
                    
                except (NoSuchElementException, StaleElementReferenceException) as e:
                    # Product tile might not have title or became stale, continue
                    continue
            
            # Product not found in current loaded products, scroll down 400px to load more
            scroll_position += scroll_amount
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            
            # Wait for lazy-loaded content to appear
            try:
                self.wait_utils.wait_for_elements_present(
                    self.product_grid_items,
                    min_count=len(products),  # Wait for at least same number of products
                    timeout=config.short_timeout
                )
            except TimeoutException:
                logger.debug("No new products loaded after scroll")
            
            # Check if we've reached the bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            current_scroll = self.driver.execute_script("return window.pageYOffset || window.scrollY || 0;")
            
            # If we're close to bottom (within 500px), we've likely loaded all products
            if current_scroll + 500 >= new_height:
                logger.debug(f"Reached bottom of page (scroll: {current_scroll}, height: {new_height})")
                break
            
            # Update last_height if page grew
            if new_height > last_height:
                last_height = new_height
        
        # Final check: scroll back to top and check all products one more time
        logger.debug("Performing final check by scrolling to top")
        self.driver.execute_script("window.scrollTo(0, 0);")
        # Wait for page to stabilize
        self.wait_utils.wait_for_elements_present(
            self.product_grid_items,
            min_count=1,
            timeout=config.short_timeout
        )
        
        products = self.driver.find_elements(*self.product_grid_items)
        for product in products:
            try:
                title_element = product.find_element(
                    By.XPATH,
                    f".//*[contains(@class,'{PRODUCT_TITLE_CLASS}')]"
                )
                if title_element.text.strip() == product_name:
                    logger.info(f"Found product '{product_name}' in final check")
                    scroll_to_element(self.driver, product)
                    return product
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        
        raise NoSuchElementException(f"Product '{product_name}' not found on collection page after scrolling")
    
    def find_and_click_product(self, product_name: str):
        """
        Find and click a product by name.
        
        Args:
            product_name: Exact product name to find and click
        
        Raises:
            NoSuchElementException: If product not found or cannot be clicked
        """
        logger.info(f"Finding and clicking product: {product_name}")
        
        try:
            # Locate product (with retry in case of staleness)
            product = self.find_product_by_name(product_name)

            # Find the anchor/link element within the product tile
            anchor = product.find_element(
                By.XPATH,
                ".//a[contains(@class,'product-grid-item')]",
            )

            # Scroll to element and click
            scroll_to_element(self.driver, anchor)
            # Wait for anchor to be clickable (handling staleness)
            WebDriverWait(self.driver, config.default_timeout).until(
                EC.element_to_be_clickable(anchor)
            )
            anchor.click()
            logger.info(f"Successfully clicked product: {product_name}")
            
        except StaleElementReferenceException:
            logger.warning("Product element became stale, retrying click once")
            # Retry once by re-finding the product and anchor
            product = self.find_product_by_name(product_name)
            anchor = product.find_element(
                By.XPATH, ".//a[contains(@class,'product-grid-item')]"
            )
            scroll_to_element(self.driver, anchor)
            WebDriverWait(self.driver, config.default_timeout).until(
                EC.element_to_be_clickable(anchor)
            )
            anchor.click()
            logger.info(f"Successfully clicked product after retry: {product_name}")

        except Exception as e:
            logger.error(f"Failed to click product '{product_name}': {str(e)}")
            raise NoSuchElementException(f"Found product '{product_name}' but could not click it: {str(e)}")
