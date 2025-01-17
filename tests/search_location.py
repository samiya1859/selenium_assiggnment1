import time
import random
from faker import Faker
from utils.read_locators import read_locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fake = Faker()
locators = read_locators()

# Helper method to wait for an element
def wait_for_element(driver, xpath, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

# Helper method to input text character by character with extra delay after the third character
def input_text_with_delay(element, text):
    for index, char in enumerate(text, start=1):
        element.send_keys(char)
        time.sleep(0.5)
        if index == len(text) :
            time.sleep(2)

# Helper method to fetch suggestions and filter by empty PID
def get_empty_pid_suggestions(suggestions_list):
    suggestions = suggestions_list.find_elements(By.XPATH, locators.get("location_sug"))
    return [s for s in suggestions if not s.get_attribute('data-pid')]

# Helper method to select and click a suggestion
def select_and_click_suggestion(wait, suggestions_list, search_input):
    empty_pid_suggestions = get_empty_pid_suggestions(suggestions_list)
    print(f"\nFound {len(empty_pid_suggestions)} suggestions with empty PID:")
    for idx, suggestion in enumerate(empty_pid_suggestions, 1):
        data_place = suggestion.get_attribute('data-place')
        print(f"{idx}. Place: {data_place} | PID: (empty)")

    if empty_pid_suggestions:
        random_suggestion = random.choice(empty_pid_suggestions)
        selected_text = random_suggestion.text
        print(f"\nSelected suggestion with empty PID: {selected_text}")
        try:
            wait.until(EC.element_to_be_clickable(random_suggestion)).click()
        except Exception as click_exception:
            print(f"Error clicking suggestion: {click_exception}. Retrying...")
            return False  # Indicate a retry is needed

        time.sleep(2)
        updated_value = search_input.get_attribute('value')
        print(f"Updated input value: {updated_value}")
        assert updated_value == selected_text, "Input field value does not match the selected suggestion."
        return True
    else:
        print("No suggestions with empty PID found.")
        return False

# Main test method
def test_search_location(driver):
    max_attempts = 5
    attempt = 0
    selected_location = None

    while attempt < max_attempts:
        try:
            search_input = wait_for_element(driver, locators.get("search_input"))
            fake_location = fake.city()
            print(f"Searching for location: {fake_location}")
            search_input.clear()
            input_text_with_delay(search_input, fake_location)

            suggestions_list = wait_for_element(driver, locators.get("sug_list"))
            if select_and_click_suggestion(WebDriverWait(driver, 10), suggestions_list, search_input):
                selected_location = search_input.get_attribute('value')
                break
            else:
                print("Generating a new city...")
                attempt += 1

            

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            attempt += 1
            if attempt >= max_attempts:
                print("Max attempts reached. Exiting the search.")
                raise
    if selected_location:
        print(f"Selected location: {selected_location}")
    return selected_location

