from utils.driver_setup import setup_driver
from utils.generate_output_xl import generate_excel
from tests.search_location import test_search_location
from tests.date_picking import select_dates_from_calendar
# from tests.property_tile_selection import click_property_tiles
from tests.property_traversing import click_property_tiles

def run_tests():
    driver = setup_driver()
    driver.maximize_window()
    url = "https://www.petfriendly.io/"
    driver.get(url)
    driver.implicitly_wait(3)

    location = test_search_location(driver)
    start_date,end_date = select_dates_from_calendar(driver)
    test_results = click_property_tiles(driver,location,start_date,end_date)

    generate_excel(key="petfriendly.io",url=url,test="check message",test_results=test_results)



    driver.quit()

if __name__ == "__main__":
    run_tests()
