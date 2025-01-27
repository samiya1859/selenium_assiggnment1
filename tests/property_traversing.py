from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .data_availability import perform_actions_on_new_tab, check_page_layout
from utils.read_locators import read_locators
import time

locators = read_locators()


def click_property_tile(driver, tile_xpath):
    """
    Scrolls the property tile into view and clicks it using JavaScript.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        tile_xpath (str): The XPath of the property tile to click.

    Returns:
        bool: True if the tile was successfully clicked, False otherwise.
    """
    # Scroll the tile into view and click using JavaScript
    property_tile = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, tile_xpath))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", property_tile)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", property_tile)
    time.sleep(3)
    return True


def generate_result_message(
    tile_id, tile_title, location, start_date, end_date, check_msg
):
    """
    Generates a result message based on the availability check result.

    Args:
        tile_id (str): The ID of the property tile.
        tile_title (str): The title of the property.
        location (str): The location for the property.
        start_date (str): The start date of the booking.
        end_date (str): The end date of the booking.
        check_msg (bool): The result of the availability check.

    Returns:
        tuple: A tuple containing the result message and the status (pass/fail).
    """
    if check_msg:
        result_message = f"Avaibility message checking Passed for {tile_id}-{tile_title} : {location}, Date: {start_date} to {end_date}"
        status = "pass"
    else:
        result_message = f"Avaibility message checking Failed for {tile_id}-{tile_title} : {location}, Date: {start_date} to {end_date}"
        status = "fail"

    return result_message, status


def click_property_tiles(driver, location, start_date, end_date, num_tiles=10):
    """
    Clicks on multiple property tiles, verifies availability in a new tab,
    and stores the results.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        location (str): The location for which properties are being searched.
        start_date (str): The start date of the booking.
        end_date (str): The end date of the booking.
        num_tiles (int, optional): The number of property tiles to process (default is 10).

    Returns:
        list: A list of dictionaries containing test results, including status,
              result message, and page information for each property.
    """
    test_results = []

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, locators.get("tile_section")))
    )

    # Loop through the specified number of tiles
    for i in range(num_tiles):

        tile_xpath = locators.get("tile").replace("{i}", str(i))
        tile_element = driver.find_element(By.XPATH, tile_xpath)
        tile_title = tile_element.text
        tile_id = tile_element.get_attribute("data-id")

        # Attempt to click the property tile link
        success = click_property_tile(driver, tile_xpath)
        if not success:
            continue

        # Wait for the new tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(2)
        page = check_page_layout(driver)
        check_msg = perform_actions_on_new_tab(driver)

        # Generate result message based on check_msg
        result_message, status = generate_result_message(
            tile_id, tile_title, location, start_date, end_date, check_msg
        )

        test_results.append(
            {
                "status": status,
                "message": result_message,
                "page": page,
            }
        )

        # Close the new tab after actions are complete
        driver.close()

        # Switch back to the refine page
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(2)

        # Wait for the property tiles section to reload, if necessary
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, locators.get("tile_section")))
        )

    return test_results
