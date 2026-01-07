from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from variables import PROJECT_LINK_XPATH, HAMBURGER_BUTTON, LAYERS_TAB, BUILD_LAYER_LABEL

class Navigation:
    def __init__(self, driver):
        self.driver = driver

    def project(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, PROJECT_LINK_XPATH))
        ).click()

    def layer_build(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, HAMBURGER_BUTTON))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, LAYERS_TAB))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, BUILD_LAYER_LABEL))).click()
