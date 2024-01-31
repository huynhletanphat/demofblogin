import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=chrome_options)
