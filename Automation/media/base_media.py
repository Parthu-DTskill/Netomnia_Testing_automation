import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseMedia:
    def __init__(self, driver):
        self.driver = driver

    def session_get(self, url, timeout=30):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return r.content
        except:
            pass
        return None

    def close_dropdown(self):
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except:
            pass
