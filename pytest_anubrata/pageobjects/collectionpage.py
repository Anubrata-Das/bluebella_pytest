"""
Collection Page Object Model.
Handles all interactions with the product collection page.
"""
import time
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
        
        # Normalize the sort option - handle both comma and colon variations
        # Also handle partial matching for "Price" options
        if "price" in sort_option.lower() and "low" in sort_option.lower():
            # Match any "Price ... Low to High" variation
            sort_option_locator = (
                By.XPATH,
                "(//div[contains(@class,'collection-filter__sorting')]//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'price') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'low')])[1]"
            )
        elif "price" in sort_option.lower() and "high" in sort_option.lower():
            # Match any "Price ... High to Low" variation
            sort_option_locator = (
                By.XPATH,
                "(//div[contains(@class,'collection-filter__sorting')]//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'price') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'high')])[1]"
            )
        else:
            # Default: use exact text match
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
        # Wait additional time for lazy content to load
        time.sleep(2)
    
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
        
        Args:
            product_name: Exact product name to find
        
        Returns:
            WebElement if found
        
        Raises:
            NoSuchElementException: If product not found
        """
        logger.info(f"Searching for product: {product_name} using incremental scrolling")
        
        max_scrolls = 100
        previous_product_count = 0
        no_new_products_count = 0
        
        # Store original implicit wait and disable it for faster element checks
        original_implicit_wait = self.driver.timeouts.implicit_wait
        self.driver.implicitly_wait(0)  # Disable implicit wait for faster iteration
        
        # Wait for product titles to be loaded (lazy rendering)
        # Scroll down to middle of page to trigger lazy loading, then back up
        self.driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Wait for at least one product with a title to appear
        title_xpath = f"//div[contains(@class,'product-grid-item-column')]//*[contains(@class,'{PRODUCT_TITLE_CLASS}')]"
        try:
            self.wait_utils.wait_for_element_present(
                (By.XPATH, title_xpath),
                timeout=15
            )
        except TimeoutException:
            logger.warning("Timed out waiting for product titles to load")
        
        try:
            for scroll_count in range(max_scrolls):
                # Get all currently loaded product elements
                products = self.driver.find_elements(*self.product_grid_items)
                current_product_count = len(products)
                
                logger.debug(f"Scroll {scroll_count + 1}: Found {current_product_count} products")
                
                if not products:
                    logger.warning("No products found on page yet")
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(0.5)
                    continue
                
                # Check each product to see if it matches
                found_titles = []
                for idx, product in enumerate(products):
                    try:
                        title_element = product.find_element(
                            By.XPATH,
                            f".//*[contains(@class,'{PRODUCT_TITLE_CLASS}')]"
                        )
                        title_text = title_element.text.strip()
                        if title_text:
                            found_titles.append(title_text)
                        
                        if title_text == product_name:
                            logger.info(f"Found matching product '{product_name}' at index {idx}")
                            scroll_to_element(self.driver, product)
                            time.sleep(0.3)
                            return product
                        
                    except (NoSuchElementException, StaleElementReferenceException):
                        continue
                
                # Log found titles for debugging (first iteration only)
                if scroll_count == 0:
                    logger.info(f"First search found {len(found_titles)} titles. First 5: {found_titles[:5]}")
                
                # Product not found yet - scroll to last product to trigger lazy loading
                last_product = products[-1]
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'end', behavior: 'instant'});",
                        last_product
                    )
                    time.sleep(0.5)
                except StaleElementReferenceException:
                    logger.debug("Last product became stale, refetching products")
                    continue
                
                # Check if new products loaded
                new_products = self.driver.find_elements(*self.product_grid_items)
                new_count = len(new_products)
                
                if new_count == previous_product_count:
                    no_new_products_count += 1
                    logger.debug(f"No new products loaded (attempt {no_new_products_count})")
                    
                    # Scroll more
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(0.5)
                    
                    if no_new_products_count >= 5:
                        logger.debug("No new products after multiple scroll attempts, reached end of page")
                        break
                else:
                    no_new_products_count = 0
                    previous_product_count = new_count
            
            # Final check: scroll back to top and check all products one more time
            logger.debug("Performing final check by scrolling to top")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
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
        
        finally:
            # Restore original implicit wait
            self.driver.implicitly_wait(original_implicit_wait)
    
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
