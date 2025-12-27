"""
Constants file for the test automation framework.
Contains reusable constants, XPath/CSS selectors, and static values.
"""

# URL Constants
BASE_URL = "https://www.bluebella.com"

# Timeout Constants (in seconds)
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 5
LONG_TIMEOUT = 20
IMPLICIT_WAIT = 5

# Browser Constants
SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]

# Common Locators
KLAVIYO_CLOSE_BUTTON = "//button[contains(@class,'klaviyo-close-form')]"

# Login Page Locators
LOGIN_HEADER_BUTTON = "//div[@class='site-header__icon--account']"
LOGIN_EMAIL_INPUT = "//input[@name='customer[email]']"
LOGIN_PASSWORD_INPUT = "//input[@name='customer[password]']"
LOGIN_SIGNIN_BUTTON = "//input[@value='Sign In']"

# Homepage Locators
MAIN_MENU_ITEMS = "//li[@js-site-header='siteNavItem']/a"

# Collection Page Locators
PRODUCT_GRID_ITEMS = "//div[contains(@class,'product-grid-item-column')]"
SORT_BY_BUTTON = "div[class='collection-filter'] button[class='collection-filter__header']"
PRODUCT_TITLE_CLASS = "product-grid-item__title"

# Product Page Locators
ADD_TO_CART_BUTTON = "//button[@id='AddToCart']"
CART_DRAWER_CLOSE_BUTTON = "//button[@class='cart-drawer__close']"
QUICK_ADD_TO_CART_BUTTON = "//div[@class='product-quick-add__container']//button[@id='AddToCart']"
CHECKOUT_BUTTON = "//div[@class='cart-drawer__footer--buttons']/a[@href='/checkout']"
COMPLETE_THE_LOOK_SECTION = "//div[@class='complete-the-look']//div[@class='owl-stage']"
COMPLETE_THE_LOOK_ITEMS = "//div[@class='complete-the-look']//div[contains(@class,'owl-item')]"
SIZE_OPTION_CLASS = "product-form__sizes--option"

# Checkout Page Locators
CHECKOUT_EMAIL_INPUT = "//input[@id='email']"
CHECKOUT_MARKETING_CHECKBOX = "//input[@id='marketing_opt_in']"
CHECKOUT_COUNTRY_DROPDOWN = "//select[@name='countryCode']"
CHECKOUT_LAST_NAME_INPUT = "//input[@name='lastName']"
CHECKOUT_FIRST_NAME_INPUT = "//input[@name='firstName']"
CHECKOUT_POSTAL_CODE_INPUT = "//input[@id='postalCode']"
CHECKOUT_POSTAL_CODE_OPTIONS = "//li[contains(@id,'postalCode-option')]"
CHECKOUT_PHONE_INPUT = "//input[@name='phone']"
CHECKOUT_PHONE_COUNTRY_DROPDOWN = "//select[@name='phone_country_select']"
CHECKOUT_KLARNA_LABEL = "//section[@aria-label='Payment']//label[@for='basic-Klarna - Flexible payments']"
CHECKOUT_PAY_BUTTON = "//button[@id='checkout-pay-button']"

# Test Data Keys
TEST_DATA_KEYS = [
    "userEmail",
    "passWord",
    "menuName",
    "subMenuName",
    "sortBy",
    "productName",
    "email",
    "lastName",
    "firstName",
    "postalCode",
    "phone",
    "phone_country_select"
]

# Payment Methods
PAYMENT_KLARNA = "Klarna - Flexible payments"

