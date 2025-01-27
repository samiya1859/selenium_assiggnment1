import time
import warnings
import random
from faker import Faker
from utils.read_locators import read_locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore", category=DeprecationWarning)
fake = Faker()
locators = read_locators()


# Helper method to wait for an element
def wait_for_element(driver, xpath, timeout=10):
    """
    Wait for an element to be present in the DOM.

    Args:
        driver: WebDriver instance.
        xpath (str): XPath of the element.
        timeout (int): Max time to wait (default: 10 seconds).

    Returns:
        WebElement: The found element.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def input_text_with_delay(element, text):
    """
    Input text into a field with delays between characters.

    Args:
        element: WebElement to input text.
        text (str): Text to input.
    """
    for index, char in enumerate(text, start=1):
        element.send_keys(char)
        time.sleep(0.5)
        if index == len(text):
            time.sleep(2)


# Helper method to fetch suggestions and filter by empty PID
def get_empty_pid_suggestions(suggestions_list):
    """
    Get suggestions with empty 'data-pid'.

    Args:
        suggestions_list: WebElement containing suggestions.

    Returns:
        list: Suggestions with empty 'data-pid'.
    """
    suggestions = suggestions_list.find_elements(By.XPATH, locators.get("location_sug"))
    return [s for s in suggestions if not s.get_attribute("data-pid")]


# Helper method to select and click a suggestion
def select_and_click_suggestion(wait, suggestions_list, search_input):
    """
    Select and click a random suggestion with empty 'data-pid'.

    Args:
        wait: WebDriverWait instance.
        suggestions_list: WebElement of suggestions.
        search_input: WebElement of the search input field.

    Returns:
        bool: True if a suggestion is selected, False otherwise.
    """
    empty_pid_suggestions = get_empty_pid_suggestions(suggestions_list)

    if empty_pid_suggestions:
        random_suggestion = random.choice(empty_pid_suggestions)
        selected_text = random_suggestion.text

        # Wait and click on the selected suggestion
        wait.until(EC.element_to_be_clickable(random_suggestion)).click()

        time.sleep(2)  # Wait for the input field to update
        updated_value = search_input.get_attribute("value")

        # Validate the updated value in the search input
        assert (
            updated_value == selected_text
        ), "Input field value does not match the selected suggestion."
        return True
    else:
        return False


def test_search_location(driver):
    """
    Test the search functionality by inputting a fake location and selecting a suggestion.

    Args:
        driver: WebDriver instance.

    Returns:
        str: The selected location, or None if no location is selected.
    """
    max_attempts = 5
    selected_location = None

    for _ in range(max_attempts):
        # Wait for the search input field
        search_input = wait_for_element(driver, locators.get("search_input"))

        # Generate a fake location and input it
        fake_location = fake.city()

        search_input.clear()
        input_text_with_delay(search_input, fake_location)

        # Wait for the suggestions list to appear
        suggestions_list = wait_for_element(driver, locators.get("sug_list"))

        # Try to select a suggestion
        if select_and_click_suggestion(
            WebDriverWait(driver, 10), suggestions_list, search_input
        ):
            selected_location = search_input.get_attribute("value")
            return selected_location  # Exit early if successful

    # If the loop finishes without selecting a location
    raise Exception("Unable to select a location.")
