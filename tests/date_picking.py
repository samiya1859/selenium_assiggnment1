from datetime import datetime, timedelta
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from utils.read_locators import read_locators


def generate_fake_dates():
    """
    Generate random start and end dates.

    Returns:
        tuple: Start date and end date strings in 'YYYY-MM-DD' format.
    """
    today = datetime.now().date()
    start_date = today + timedelta(days=random.randint(0, 15))
    end_date = start_date + timedelta(days=random.randint(1, 15))

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date, end_date, start_date_str, end_date_str


def select_dates_from_calendar(driver):
    """
    Select start and end dates from the calendar widget.

    Args:
        driver: WebDriver instance.

    Returns:
        tuple: Start date and end date strings in 'YYYY-MM-DD' format.
    """

    locators = read_locators()  # Load locators
    date_xpath_template = locators.get("date")  # Get date XPath template
    confirm_btn_locator = locators.get("confirm_btn")  # Get confirm button locator
    # Generate fake dates
    start_date, end_date, start_date_str, end_date_str = generate_fake_dates()
    # Wait for the calendar to be visible
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "datepicker__months")))
    actions = ActionChains(driver)
    # Select start date
    start_day = str(start_date.day)
    for month in range(1, 3):  # Check months 1 and 2 (e.g., current and next month)
        try:
            start_xpath = date_xpath_template.format(month=month, day=start_day)
            start_element = driver.find_element(By.XPATH, start_xpath.strip())
            if start_element.is_displayed():
                actions.move_to_element(start_element).click().perform()
                break
        except NoSuchElementException:
            continue
    # Select end date
    end_day = str(end_date.day)
    for month in range(1, 3):
        try:
            end_xpath = date_xpath_template.format(month=month, day=end_day)
            end_element = driver.find_element(By.XPATH, end_xpath.strip())
            if end_element.is_displayed():
                actions.move_to_element(end_element).click().perform()
                break
        except NoSuchElementException:
            continue
    # Confirm date selection
    confirm_button = wait.until(
        EC.element_to_be_clickable((By.ID, confirm_btn_locator))
    )
    confirm_button.click()
    return start_date_str, end_date_str
