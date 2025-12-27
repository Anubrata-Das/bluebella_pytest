"""
Pytest configuration and fixtures.
Contains shared fixtures and hooks for the test framework.
"""
import os
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from config.config_manager import config
from utils.logger import get_logger

logger = get_logger()


# ============================
# Pytest CLI Options
# ============================

def pytest_addoption(parser):
    """
    Add custom command line options for pytest.
    
    Options:
        --browser_name: Browser to use (chrome, firefox)
        --headless: Run browser in headless mode
    """
    parser.addoption(
        "--browser_name",
        action="store",
        default=config.default_browser,
        choices=["chrome", "firefox"],
        help="Browser to use for testing (chrome, firefox)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


# ============================
# Browser Fixture
# ============================

@pytest.fixture(scope="function")
def browser_instance(request):
    """
    Fixture to create and manage WebDriver instance.
    
    Yields:
        WebDriver instance
    
    Teardown:
        Quits the browser after test completion
    """
    browser_name = request.config.getoption("--browser_name")
    headless = request.config.getoption("--headless")
    
    logger.info(f"Initializing {browser_name} browser (headless={headless})")
    driver = None
    
    try:
        if browser_name == "chrome":
            driver = _create_chrome_driver(headless)
        elif browser_name == "firefox":
            driver = _create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Set implicit wait
        driver.implicitly_wait(config.implicit_wait)
        logger.info(f"Browser initialized successfully: {driver.current_url if hasattr(driver, 'current_url') else 'N/A'}")
        
        yield driver
        
    except Exception as e:
        logger.error(f"Error during browser setup: {e}")
        raise
    finally:
        if driver:
            logger.info("Closing browser")
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")


def _create_chrome_driver(headless: bool = False):
    """
    Create Chrome WebDriver instance.
    
    Args:
        headless: Whether to run in headless mode
    
    Returns:
        Chrome WebDriver instance
    """
    options = ChromeOptions()
    
    # Get Chrome options from config
    chrome_options_str = config.get("Browser", "chrome_options", "")
    if chrome_options_str:
        for option in chrome_options_str.split(","):
            if option.strip():
                options.add_argument(option.strip())
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        logger.debug("Chrome running in headless mode")
    
    # Additional Chrome options for stability
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver
    except Exception as e:
        logger.error(f"Failed to create Chrome driver: {e}")
        raise


def _create_firefox_driver(headless: bool = False):
    """
    Create Firefox WebDriver instance.
    
    Args:
        headless: Whether to run in headless mode
    
    Returns:
        Firefox WebDriver instance
    """
    options = FirefoxOptions()
    
    # Get Firefox options from config
    firefox_options_str = config.get("Browser", "firefox_options", "")
    if firefox_options_str:
        for option in firefox_options_str.split(","):
            if option.strip():
                options.add_argument(option.strip())
    
    if headless:
        options.add_argument("--headless")
        logger.debug("Firefox running in headless mode")
    
    try:
        driver = webdriver.Firefox(options=options)
        # Set window size if not headless
        if not headless:
            driver.set_window_size(1920, 1080)
        return driver
    except Exception as e:
        logger.error(f"Failed to create Firefox driver: {e}")
        raise


# ============================
# Pytest Configuration
# ============================

def pytest_configure(config):
    """
    Configure pytest settings.
    Sets up HTML reporting if pytest-html is available.
    """
    # Configure HTML report
    if not hasattr(config.option, "htmlpath") or not config.option.htmlpath:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = config.reports_path / f"report_{timestamp}.html"
        config.option.htmlpath = str(report_file)
        logger.info(f"HTML report will be generated at: {report_file}")
    
    # Make report self-contained (embeds images)
    if hasattr(config.option, "self_contained_html"):
        config.option.self_contained_html = True


# ============================
# Pytest Hooks
# ============================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    Adds screenshots to HTML reports when tests fail.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    
    # Only process actual test execution, not setup/teardown
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        
        # Handle failed tests or unexpected passes in xfail scenarios
        if (report.failed and not xfail) or (report.skipped and xfail):
            # Only take screenshot if test uses browser_instance fixture
            if "browser_instance" in item.fixturenames:
                driver = item.funcargs.get("browser_instance")
                
                if driver:
                    screenshot_path = _take_screenshot(driver, item, report)
                    if screenshot_path:
                        _add_screenshot_to_report(item, extra, screenshot_path)
    
    report.extra = extra


def _take_screenshot(driver, item, report):
    """
    Take screenshot on test failure.
    
    Args:
        driver: WebDriver instance
        item: Test item
        report: Test report
    
    Returns:
        Path to screenshot file, or None if failed
    """
    try:
        # Create screenshots directory
        screenshot_dir = config.screenshots_path
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate screenshot filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_name = report.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
        filename = f"{test_name}_{timestamp}.png"
        file_path = screenshot_dir / filename
        
        # Take screenshot
        driver.save_screenshot(str(file_path))
        logger.info(f"Screenshot saved: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        return None


def _add_screenshot_to_report(item, extra, screenshot_path):
    """
    Add screenshot to HTML report.
    
    Args:
        item: Test item
        extra: Report extra data list
        screenshot_path: Path to screenshot file
    """
    try:
        html = item.config.pluginmanager.getplugin("html")
        if html:
            extra.append(html.extras.image(str(screenshot_path), mime_type="image/png"))
            extra.append(html.extras.text(f"Screenshot: {screenshot_path}"))
    except Exception as e:
        logger.warning(f"Failed to add screenshot to report: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """
    Log test setup information.
    """
    logger.info(f"Starting test: {item.nodeid}")
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    """
    Log test teardown information.
    """
    yield
    logger.info(f"Completed test: {item.nodeid}")
