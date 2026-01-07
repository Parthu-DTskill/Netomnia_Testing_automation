import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from variables import LOGIN_BUTTON, smart_find_element

class Login:
    def __init__(self, driver, url, username, password):
        self.driver = driver
        self.url = url
        self.username = username
        self.password = password

    def execute(self):
        self.driver.get(self.url)
        time.sleep(3)

        user = smart_find_element(self.driver, ["email", "username"], tag="input")
        pwd = smart_find_element(self.driver, ["password", "pwd"], tag="input")

        if user:
            user.clear()
            user.send_keys(self.username)

        if pwd:
            pwd.clear()
            pwd.send_keys(self.password)

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON))
        ).click()
