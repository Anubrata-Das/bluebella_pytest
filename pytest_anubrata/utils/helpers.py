"""
Helper utilities for test automation framework.
Contains reusable helper functions for common operations.
"""
import json
from pathlib import Path
from typing import Dict, List, Any

from config.config_manager import config
from utils.logger import get_logger

logger = get_logger()


def load_test_data(file_path: Path = None) -> List[Dict[str, Any]]:
    """
    Load test data from JSON file.
    
    Args:
        file_path: Path to JSON file (defaults to config path)
    
    Returns:
        List of test data dictionaries
    
    Raises:
        FileNotFoundError: If test data file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    if file_path is None:
        file_path = config.test_data_path
    
    if not file_path.exists():
        raise FileNotFoundError(f"Test data file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            test_data_list = data.get('data', [])
            logger.info(f"Loaded {len(test_data_list)} test data sets from {file_path}")
            return test_data_list
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in test data file: {e}")
        raise


def validate_test_data(test_data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate that test data contains all required keys.
    
    Args:
        test_data: Test data dictionary
        required_keys: List of required key names
    
    Returns:
        True if all keys present, False otherwise
    """
    missing_keys = [key for key in required_keys if key not in test_data]
    if missing_keys:
        logger.warning(f"Missing required keys in test data: {missing_keys}")
        return False
    return True


def get_screenshot_path(test_name: str) -> Path:
    """
    Generate screenshot file path.
    
    Args:
        test_name: Name of the test
    
    Returns:
        Path object for screenshot file
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_test_name = test_name.replace("::", "_").replace("/", "_").replace("\\", "_")
    filename = f"{safe_test_name}_{timestamp}.png"
    return config.screenshots_path / filename


def scroll_to_element(driver, element):
    """
    Scroll element into view using JavaScript.
    
    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
        element
    )
    logger.debug("Scrolled to element")


def wait_for_page_load(driver, timeout=10):
    """
    Wait for page to fully load.
    
    Args:
        driver: WebDriver instance
        timeout: Maximum time to wait
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logger.debug("Page loaded completely")
    except Exception as e:
        logger.warning(f"Page load timeout: {e}")


def safe_find_element(driver, locator, timeout=2):
    """
    Safely find element without raising exception.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, locator_string)
        timeout: Short timeout for quick check
    
    Returns:
        WebElement if found, None otherwise
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None

