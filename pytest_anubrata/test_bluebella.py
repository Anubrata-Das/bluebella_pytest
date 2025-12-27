"""
End-to-End Test Suite for Bluebella E-commerce Website.
Tests complete user journey from login to checkout.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pageobjects.login import LoginPage
from pageobjects.homepage import HomePage
from pageobjects.collectionpage import CollectionPage
from pageobjects.productpage import ProductPage
from pageobjects.checkoutpage import CheckoutPage
from config.config_manager import config
from utils.helpers import load_test_data, validate_test_data
from utils.constants import TEST_DATA_KEYS, KLAVIYO_CLOSE_BUTTON
from utils.logger import get_logger

logger = get_logger()

# Load test data once at module level
test_data_list = load_test_data()


@pytest.mark.smoke
@pytest.mark.parametrize("test_data", test_data_list, ids=lambda data: f"{data.get('productName', 'Unknown')}")
def test_bluebella_e2e_shopping_flow(browser_instance, test_data):
    """
    End-to-end test for Bluebella shopping flow.
    
    Test Steps:
    1. Navigate to homepage and close popups
    2. Login with user credentials
    3. Navigate to product collection via menu
    4. Sort products and select a specific product
    5. Add products to cart
    6. Proceed to checkout and fill form
    7. Select payment method and complete checkout
    
    Args:
        browser_instance: WebDriver fixture
        test_data: Test data dictionary from JSON file
    """
    driver = browser_instance
    
    # Validate test data
    assert validate_test_data(test_data, TEST_DATA_KEYS), \
        f"Test data missing required keys. Required: {TEST_DATA_KEYS}"
    
    logger.info(f"Starting E2E test for product: {test_data.get('productName')}")
    
    try:
        # Step 1: Navigate to homepage
        logger.info("Step 1: Navigating to homepage")
        homepage = HomePage(driver)
        homepage.navigate_to(config.base_url)
        original_url = homepage.get_current_url()
        
        # Close Klaviyo popup if present
        homepage.close_klaviyo_popup()
        
        # Step 2: Login
        logger.info("Step 2: Performing login")
        login_page = LoginPage(driver)
        assert login_page.get_title(), "Page title should not be empty"
        
        login_page.login(
            username=test_data["userEmail"],
            password=test_data["passWord"]
        )
        
        # Verify login successful
        assert login_page.is_signed_in(), "Login should be successful"
        login_page.navigate_back_to_homepage(original_url)
        
        # Step 3: Navigate to product collection
        logger.info("Step 3: Navigating to product collection")
        homepage.hover_to_menu(
            menu_name=test_data["menuName"],
            sub_menu_name=test_data["subMenuName"]
        )
        
        # Verify navigation to collection page
        current_url = driver.current_url
        assert "collection" in current_url.lower() or current_url != original_url, \
            "Should navigate to collection page"
        
        # Step 4: Sort and select product
        logger.info("Step 4: Sorting and selecting product")
        collection_page = CollectionPage(driver)
        collection_page.sort_by_text(test_data["sortBy"])
        
        collection_page.find_and_click_product(test_data["productName"])
        
        # Verify navigation to product page
        product_url = driver.current_url
        assert test_data["productName"].lower().replace(" ", "-") in product_url.lower() or \
               "product" in product_url.lower(), \
            "Should navigate to product detail page"
        
        # Step 5: Add products to cart
        logger.info("Step 5: Adding products to cart")
        product_page = ProductPage(driver)
        
        # Select sizes if available
        product_page.select_size_if_available("38")
        product_page.select_size_if_available("D")
        
        # Add first item and close drawer
        product_page.add_to_cart_and_close_drawer()
        
        # Add item from "Complete the Look" section
        try:
            product_page.click_last_complete_the_look_item()
        except (TimeoutException, NoSuchElementException) as e:
            logger.warning(f"Complete the Look section not available: {e}")
        
        # Quick add another size
        product_page.select_quick_add_size_if_available("M")
        product_page.proceed_to_checkout()
        
        # Step 6: Fill checkout form
        logger.info("Step 6: Filling checkout form")
        checkout_page = CheckoutPage(driver)
        
        # Verify on checkout page
        checkout_url = driver.current_url
        assert "checkout" in checkout_url.lower(), "Should be on checkout page"
        
        checkout_page.fill_checkout_form(
            email=test_data["email"],
            last_name=test_data["lastName"],
            first_name=test_data["firstName"],
            postal_code=test_data["postalCode"],
            phone=test_data["phone"],
            phone_country_code=test_data["phone_country_select"],
            country=test_data.get("country", "Japan"),
            postal_search_text=test_data.get("postalSearchText", "Iguchi")
        )
        
        # Step 7: Select payment and complete checkout
        logger.info("Step 7: Completing checkout with payment")
        checkout_page.complete_checkout_with_klarna()
        
        logger.info("E2E test completed successfully")
        
    except AssertionError as e:
        logger.error(f"Test assertion failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        raise


# Additional test markers can be added for different test types
# @pytest.mark.regression
# @pytest.mark.sanity
