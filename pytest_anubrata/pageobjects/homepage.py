"""
Homepage Page Object Model.
Handles all interactions with the homepage.
"""
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from pageobjects.base_page import BasePage
from utils.constants import MAIN_MENU_ITEMS, KLAVIYO_CLOSE_BUTTON
from utils.logger import get_logger

logger = get_logger()


class HomePage(BasePage):
    """Page Object for Homepage functionality."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize HomePage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.menu_items = (By.XPATH, MAIN_MENU_ITEMS)
        self.klaviyo_close_button = (By.XPATH, KLAVIYO_CLOSE_BUTTON)
    
    def close_klaviyo_popup(self):
        """Close Klaviyo popup if present."""
        try:
            if self.is_element_visible(self.klaviyo_close_button, timeout=3):
                logger.info("Closing Klaviyo popup")
                self.click_element(self.klaviyo_close_button)
                return True
        except Exception as e:
            logger.debug(f"Klaviyo popup not present or already closed: {e}")
        return False
    
    def hover_to_menu(self, menu_name: str, sub_menu_name: str):
        """
        Hover over main menu and click submenu.
        
        Args:
            menu_name: Name of the main menu item
            sub_menu_name: Name of the submenu item to click
        
        Raises:
            NoSuchElementException: If menu or submenu not found
        """
        logger.info(f"Hovering to menu: {menu_name} -> {sub_menu_name}")
        action_chains = ActionChains(self.driver)
        
        # Wait for menu items to be present
        menu_elements = self.wait_utils.wait_for_elements_present(self.menu_items)
        
        menu_found = False
        for menu_nav in menu_elements:
            if menu_nav.text.strip() == menu_name:
                logger.debug(f"Found menu item: {menu_name}")
                menu_found = True
                
                # Hover on the menu item
                action_chains.move_to_element(menu_nav).perform()
                
                # Find submenu within the same menu block
                try:
                    submenu = menu_nav.find_element(
                        By.XPATH,
                        f"./ancestor::li[@js-site-header='siteNavItem']//a[normalize-space()='{sub_menu_name}']"
                    )
                    logger.info(f"Found submenu: {sub_menu_name}")
                    submenu.click()
                    return
                except NoSuchElementException:
                    logger.error(f"Submenu '{sub_menu_name}' not found under '{menu_name}'")
                    raise
        
        if not menu_found:
            raise NoSuchElementException(f"Menu item '{menu_name}' not found")