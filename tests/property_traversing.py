from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from .data_avaibility import perform_actions_on_new_tab, check_page_layout
import time
import traceback
from utils.read_locators import read_locators

locators = read_locators()

def click_property_tile(driver, tile_xpath):
    # Scroll the tile into view and click using JavaScript
    property_tile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, tile_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", property_tile)
    time.sleep(1)  # Adding a small delay to ensure the element is fully loaded
    try:
        driver.execute_script("arguments[0].click();", property_tile)
        time.sleep(3)
        return True
    except (StaleElementReferenceException, ElementClickInterceptedException) as e:
        print(f"Exception occurred: {str(e)}")
        return False

def click_property_tiles(driver,location,start_date,end_date, num_tiles=10):

    test_results = []
    # Wait for the js-tiles-container to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, locators.get("tile_section"))))
        print("Property tiles container loaded.")
    except TimeoutException:
        print("Timed out waiting for the property tiles container to load.")
        return

    # Loop through the specified number of tiles
    for i in range(num_tiles):
        try:
            # Constructing the XPath for the anchor tag inside the details/title structure
            tile_xpath = f"//div[@id='js-item-{i}']//div[contains(@class, 'details')]//div[contains(@class, 'title')]//a"
            print(f"Looking for tile link with XPath: {tile_xpath}")

            # Attempt to click the property tile link
            success = click_property_tile(driver, tile_xpath)
            if not success:
                continue

            # Wait for the new tab to open
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            print("New tab opened.")

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])
            print(f"Switched to the new tab: {driver.current_window_handle}")

            time.sleep(2)
            page = check_page_layout(driver)
            check_msg = perform_actions_on_new_tab(driver)

            # Generate result message based on check_msg
            if check_msg:
                result_message = f"Passed for {location}, Date: {start_date} to {end_date}"
                status = "pass"
            else:
                result_message = f"Failed for {location}, Date: {start_date} to {end_date}"
                status = "fail"

            test_results.append({
                "status": status,
                "message": result_message,
                "page": page,
            })
            

            # Close the new tab after actions are complete
            driver.close()
            print("Closed the new tab.")

            # Switch back to the refine page
            driver.switch_to.window(driver.window_handles[0])
            print(f"Switched back to the main tab: {driver.current_window_handle}")
            time.sleep(2)

            # Wait for the property tiles section to reload, if necessary
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, locators.get("tile_section"))))

        except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"Encountered an exception for property tile js-item-{i}: {str(e)}. Retrying...")
            print(traceback.format_exc())
            continue
        except Exception as e:
            print(f"An unexpected error occurred for tile {i}: {str(e)}")
            print(traceback.format_exc())
            continue
    
    return test_results