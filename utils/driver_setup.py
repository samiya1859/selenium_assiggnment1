from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def setup_driver():
    # WebDriver setup
    chromedriver_path = "/home/w3e11/Downloads/chromedriver-linux64/chromedriver"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    
    return driver
