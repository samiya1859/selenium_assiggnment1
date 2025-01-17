from datetime import datetime, timedelta  
import random  
import time
from utils.read_locators import read_locators
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains  



def select_dates_from_calendar(driver):
    """Select dates and verify page layout"""
    test_results = []
    locators = read_locators()
    try:
        # Generate random dates
        today = datetime.now().date()
        start_date = today + timedelta(days=random.randint(0, 15))
        end_date = start_date + timedelta(days=random.randint(1, 15))
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        print(f"Generated dates - Start: {start_date_str}, End: {end_date_str}")
        
        # Wait for calendar
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "datepicker__months")))
        
        date_xpath_template = """
            //div[contains(@class, 'datepicker__months')]
            //table[contains(@id, 'month-{month}-js-date-range')]
            //tbody//tr[contains(@class, 'datepicker__week-row')]
            //td[contains(@class, 'datepicker__month-day--valid') and text()='{day}']
        """
        # date_xpath_template = locators.get("date")

        actions = ActionChains(driver)
        
        # Select start date with proper hover
        start_day = str(start_date.day)
        start_element = None
        for month in [1, 2]:
            try:
                start_xpath = date_xpath_template.format(month=month, day=start_day)
                start_element = driver.find_element(By.XPATH, start_xpath.strip())
                if start_element.is_displayed():
                    actions.move_to_element(start_element)
                    actions.click()
                    actions.perform()
                    print(f"Selected start date in month {month}")
                    break
            except:
                continue
        
        time.sleep(1)  # Small pause after start date selection
        
        # Get all dates between start and end for hovering
        current_date = start_date
        while current_date <= end_date:
            current_day = str(current_date.day)
            for month in [1, 2]:
                try:
                    current_xpath = date_xpath_template.format(month=month, day=current_day)
                    current_element = driver.find_element(By.XPATH, current_xpath.strip())
                    if current_element.is_displayed():
                        actions.move_to_element(current_element)
                        actions.perform()
                        time.sleep(0.1)  # Small delay for visible hover effect
                        break
                except:
                    continue
            current_date += timedelta(days=1)
        
        # Select end date
        end_day = str(end_date.day)
        for month in [1, 2]:
            try:
                end_xpath = date_xpath_template.format(month=month, day=end_day)
                end_element = driver.find_element(By.XPATH, end_xpath.strip())
                if end_element.is_displayed():
                    actions.move_to_element(end_element)
                    actions.click()
                    actions.perform()
                    time.sleep(2)
                    print(f"Selected end date in month {month}")
                    break
            except:
                continue
        
         # Wait for and click the confirm button
        time.sleep(1)  # Small pause before clicking button
        confirm_button = wait.until(
            EC.element_to_be_clickable((By.ID, locators.get("confirm_btn")))
        )
        confirm_button.click()
        print("Confirmed date selection")
        
        # After date selection and continue button click
        time.sleep(3)
        return start_date_str,end_date_str
        
        
        
    except Exception as e:
        print("found error while picking date")