# Bluebella E-commerce Test Automation Framework

A comprehensive, enterprise-ready Selenium WebDriver test automation framework built with Python and pytest for testing the Bluebella e-commerce website.

## 🎯 Overview

This framework implements industry best practices for test automation, including:
- **Page Object Model (POM)** pattern for maintainable code
- **Configuration Management** for centralized settings
- **Comprehensive Logging** for debugging and traceability
- **Explicit Waits** for reliable test execution
- **Parameterized Tests** for data-driven testing
- **HTML Reporting** with screenshots on failure
- **Cross-browser Support** (Chrome, Firefox)

## 📁 Project Structure

```
PythonProject/
├── data/
│   └── bluebella_automation_data.json    # Test data (JSON format)
├── pytest_anubrata/
│   ├── config/
│   │   ├── config.ini                    # Configuration file
│   │   ├── config_manager.py            # Configuration manager
│   │   └── __init__.py
│   ├── pageobjects/                     # Page Object Model classes
│   │   ├── base_page.py                # Base page class
│   │   ├── login.py                    # Login page
│   │   ├── homepage.py                 # Homepage
│   │   ├── collectionpage.py           # Product collection page
│   │   ├── productpage.py              # Product detail page
│   │   ├── checkoutpage.py             # Checkout page
│   │   └── __init__.py
│   ├── utils/                          # Utility modules
│   │   ├── constants.py                # Constants and locators
│   │   ├── logger.py                   # Logging utility
│   │   ├── waits.py                    # Wait utilities
│   │   ├── helpers.py                  # Helper functions
│   │   └── __init__.py
│   ├── conftest.py                     # Pytest fixtures and hooks
│   ├── test_bluebella.py               # Main test file
│   ├── reports/                        # HTML test reports
│   ├── screenshots/                    # Failure screenshots
│   └── logs/                           # Execution logs
├── pytest.ini                          # Pytest configuration
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Chrome or Firefox browser** (latest version recommended)

3. **ChromeDriver/GeckoDriver** (if not using webdriver-manager)
   - ChromeDriver: https://chromedriver.chromium.org/
   - GeckoDriver: https://github.com/mozilla/geckodriver/releases

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd C:\Users\Computer\PycharmProjects\PythonProject
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   pytest --version
   ```

## ⚙️ Configuration

### Config File (`pytest_anubrata/config/config.ini`)

The framework uses a centralized configuration file for all settings:

```ini
[DEFAULT]
base_url = https://www.bluebella.com
timeout = 10

[Browser]
default_browser = chrome
chrome_options = --start-maximized,--disable-blink-features=AutomationControlled

[Paths]
test_data_path = data/bluebella_automation_data.json
screenshots_path = pytest_anubrata/screenshots
reports_path = pytest_anubrata/reports
logs_path = pytest_anubrata/logs
```

### Test Data (`data/bluebella_automation_data.json`)

Test data is stored in JSON format for easy maintenance:

```json
{
  "data": [
    {
      "userEmail": "user@example.com",
      "passWord": "password123",
      "menuName": "Lingerie",
      "subMenuName": "All Lingerie",
      "sortBy": "Newest",
      "productName": "Product Name",
      "email": "checkout@example.com",
      "lastName": "Last",
      "firstName": "First",
      "postalCode": "181",
      "phone": "+1234567890",
      "phone_country_select": "US",
      "country": "United States",
      "postalSearchText": "SearchText"
    }
  ]
}
```

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest pytest_anubrata/test_bluebella.py

# Run with verbose output
pytest -v

# Run specific test by name
pytest pytest_anubrata/test_bluebella.py::test_bluebella_e2e_shopping_flow
```

### Browser Selection

```bash
# Run with Chrome (default)
pytest --browser_name=chrome

# Run with Firefox
pytest --browser_name=firefox

# Run in headless mode
pytest --headless
```

### Test Markers

```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Exclude specific markers
pytest -m "not smoke"
```

### Parallel Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

### Report Generation

HTML reports are automatically generated in the `pytest_anubrata/reports/` directory.

```bash
# Generate HTML report with custom name
pytest --html=reports/my_report.html

# Self-contained HTML report (includes all assets)
pytest --html=reports/report.html --self-contained-html
```

## 📊 Test Reports

### HTML Reports

- Location: `pytest_anubrata/reports/`
- Contains: Test results, execution time, pass/fail status
- Features: Screenshots embedded for failed tests

### Logs

- Location: `pytest_anubrata/logs/`
- Format: Daily log files with timestamps
- Contains: Detailed execution logs, debug information

### Screenshots

- Location: `pytest_anubrata/screenshots/`
- Triggered: Automatically on test failure
- Format: PNG files with test name and timestamp

## 🏗️ Framework Architecture

### Page Object Model (POM)

Each page has its own class encapsulating:
- **Locators**: XPath/CSS selectors
- **Methods**: Page-specific actions
- **Inheritance**: All pages inherit from `BasePage`

**Example:**
```python
class LoginPage(BasePage):
    def login(self, username, password):
        self.click_account_icon()
        self.enter_email(username)
        self.enter_password(password)
        self.click_signin_button()
```

### Base Page Class

Provides common functionality:
- Element interactions (click, send_keys, etc.)
- Wait utilities
- Navigation methods
- Logging integration

### Wait Strategies

The framework uses explicit waits instead of hardcoded sleeps:

```python
# Wait for element to be visible
self.wait_utils.wait_for_element_visible(locator)

# Wait for element to be clickable
self.wait_utils.wait_for_element_clickable(locator)

# Check if element exists (no exception)
self.is_element_visible(locator, timeout=2)
```

### Logging System

Centralized logging with:
- File logging (daily rotation)
- Console logging
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Formatted output with timestamps

## 🔧 Key Features

### 1. Configuration Management
- Centralized config file
- Environment-specific settings
- Easy to maintain and update

### 2. Robust Error Handling
- Explicit waits for elements
- Try-except blocks for optional elements
- Meaningful error messages

### 3. Data-Driven Testing
- JSON-based test data
- Parameterized tests
- Easy to add new test scenarios

### 4. Reporting and Logging
- HTML reports with screenshots
- Detailed execution logs
- Failure analysis support

### 5. Maintainability
- Page Object Model pattern
- Reusable utilities
- Clear separation of concerns
- Constants for locators

## 🎓 Best Practices Implemented

1. ✅ **No Hardcoded Values**: All values come from config or test data
2. ✅ **No time.sleep()**: Uses explicit waits throughout
3. ✅ **Proper Logging**: Comprehensive logging at all levels
4. ✅ **Error Handling**: Graceful handling of exceptions
5. ✅ **Code Reusability**: Common functions in base classes
6. ✅ **Documentation**: Docstrings and comments throughout
7. ✅ **Test Organization**: Clear structure and naming conventions
8. ✅ **CI/CD Ready**: Can be integrated with Jenkins, GitLab CI, etc.

## 📝 Adding New Tests

### 1. Add Test Data

Edit `data/bluebella_automation_data.json`:

```json
{
  "data": [
    {
      "userEmail": "newuser@example.com",
      ...
    }
  ]
}
```

### 2. Create Page Object (if needed)

Create new page class in `pytest_anubrata/pageobjects/`:

```python
from pageobjects.base_page import BasePage

class NewPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.element_locator = (By.XPATH, "//div[@id='element']")
    
    def perform_action(self):
        self.click_element(self.element_locator)
```

### 3. Write Test

Add test method to test file:

```python
@pytest.mark.regression
def test_new_feature(browser_instance, test_data):
    # Test implementation
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **WebDriver not found**
   - Ensure ChromeDriver/GeckoDriver is in PATH
   - Or install webdriver-manager: `pip install webdriver-manager`

2. **Element not found errors**
   - Check if locators are correct
   - Verify element is visible/clickable
   - Increase timeout in config if needed

3. **Tests timing out**
   - Check network connectivity
   - Verify website is accessible
   - Review wait strategies

4. **Import errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   - Check Python path configuration

## 📚 Interview Talking Points

When discussing this project in interviews, highlight:

1. **Architecture**: Page Object Model pattern, base classes, inheritance
2. **Configuration Management**: Centralized config, environment handling
3. **Wait Strategies**: Explicit waits vs implicit waits vs hardcoded sleeps
4. **Error Handling**: Try-except blocks, meaningful error messages
5. **Logging**: Structured logging, different log levels
6. **Reporting**: HTML reports, screenshots, CI/CD integration
7. **Maintainability**: Code organization, reusability, documentation
8. **Best Practices**: No hardcoded values, data-driven testing, test markers

## 🔄 CI/CD Integration

This framework can be easily integrated with CI/CD pipelines:

```yaml
# Example GitLab CI configuration
test:
  script:
    - pip install -r requirements.txt
    - pytest --browser_name=chrome --headless --html=reports/report.html
  artifacts:
    paths:
      - pytest_anubrata/reports/
      - pytest_anubrata/screenshots/
```

## 👥 Contributing

When extending this framework:

1. Follow the existing code structure
2. Add appropriate logging
3. Update documentation
4. Maintain code quality standards
5. Write clear, descriptive commit messages

## 📄 License

This project is for demonstration and learning purposes.

## 🙏 Acknowledgments

- Built with [Selenium WebDriver](https://www.selenium.dev/)
- Test framework: [pytest](https://docs.pytest.org/)
- Reporting: [pytest-html](https://github.com/pytest-dev/pytest-html)

---

**Note**: This framework is designed for educational and demonstration purposes. For production use, consider adding additional features like:
- API testing integration
- Database validation
- Performance testing
- Visual regression testing
- Test data management tools
- Test execution in cloud (Sauce Labs, BrowserStack)

