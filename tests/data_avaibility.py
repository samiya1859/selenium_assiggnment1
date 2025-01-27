from selenium.webdriver.common.by import By
from .search_location import wait_for_element
from utils.read_locators import read_locators, read_msg
import time

locators = read_locators()
message = read_msg()


def check_page_layout(driver):
    """
    Retrieves the value of the `pageLayout` variable from the page using JavaScript.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        str or None: The `pageLayout` value if present, otherwise None.
    """

    page_layout = driver.execute_script("return window.ScriptData.pageLayout;")
    return page_layout if page_layout else None


def perform_actions_on_new_tab(driver):
    """
    Checks if the expected availability message appears in the date availability section.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if the expected message is found in the available date element,
              otherwise False.
    """
    check_msg = False

    # Wait for the availability box and check for date elements

    availability_box = wait_for_element(driver, locators.get("msg_check_box"))
    date_available_xpath = locators.get("date_success")
    date_available = availability_box.find_element(By.XPATH, date_available_xpath)
    expected_text = message.get("expected_msg")

    # Check if the date available element contains the expected message
    if date_available.is_displayed() and expected_text in date_available.text:
        check_msg = True

    time.sleep(2)

    return check_msg
