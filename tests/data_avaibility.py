from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
import time
import traceback
from utils.read_locators import read_locators, read_msg

locators = read_locators()
message =  read_msg()

def check_page_layout(driver):
    """
    Checks the page layout using JavaScript variable `window.ScriptData.pageLayout`.
    Returns the value of `pageLayout` if found, otherwise returns None.
    """
    try:
        page_layout = driver.execute_script("return window.ScriptData.pageLayout;")
        if page_layout:
            print(f"Page layout detected: {page_layout}")
            return page_layout
        else:
            print("Page layout variable is not defined or empty.")
            return None
    except Exception as e:
        print(f"An error occurred while checking page layout: {str(e)}")
        return None

def perform_actions_on_new_tab(driver):
    
    check_msg = False

    try:
        # Wait for the availability box to be present
        availability_box_xpath = locators.get("msg_check_box")
        availability_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, availability_box_xpath)))
        print("Availability box is present.")

        # Check the visibility of the date availability elements
        date_available_xpath = locators.get("date_success")
        date_unavailable_xpath = locators.get("date_fail")

        date_available = availability_box.find_element(By.XPATH, date_available_xpath)
        date_unavailable = availability_box.find_element(By.XPATH, date_unavailable_xpath)

        expected_text = message.get("expected_msg")
        print(expected_text)

        if date_available.is_displayed():
            date_available_text = date_available.text
            print(date_available_text)
            if expected_text in date_available_text:
                print("Dates selected are available.")
                check_msg = True
            else:
                print(f"Expected text not found. Found text: {date_available_text}")
        elif date_unavailable.is_displayed():
            print("Dates selected are not available.")
        else:
            print("Unable to determine the availability of the selected dates.")


        
        time.sleep(2)  # Adding a delay to simulate more actions

        return check_msg

    except Exception as e:
        print(f"An error occurred while performing actions on the new tab: {str(e)}")
        print(traceback.format_exc())