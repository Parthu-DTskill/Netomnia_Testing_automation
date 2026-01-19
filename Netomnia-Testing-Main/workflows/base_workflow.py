import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from variables import FEATURES_TAB, CLEAR_SEARCH_BUTTON, ABS_XPATH


class BaseWorkflow:
    
    def __init__(self, driver, rows, root_folder, rejections):
        self.driver = driver
        self.rows = rows
        self.root_folder = root_folder
        self.rejections = rejections

    def get_feature_folder(self, row):
        path = os.path.join(
            self.root_folder,
            f"{row['Assessor']} - {row['Polygon Type']} {row['Town']} {row['Contractor AFP ref']}",
            row["code"],
            str(row["Feature ID"])
        )
        os.makedirs(path, exist_ok=True)
        return path

    def open_feature_type(self, option_xpath, wait_time=20):

        wait = WebDriverWait(self.driver, wait_time)

        features_tab = wait.until(EC.presence_of_element_located((By.XPATH, FEATURES_TAB)))
        self.driver.execute_script("arguments[0].click();", features_tab)

        try:
            clear_search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, CLEAR_SEARCH_BUTTON)))
            self.driver.execute_script("arguments[0].click();", clear_search_btn)
            time.sleep(1)
        except:
            pass

        dropdown_panel = wait.until(EC.presence_of_element_located((By.XPATH, ABS_XPATH)))
        dropdown_panel.click()
        time.sleep(1)

        option = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
        self.driver.execute_script("arguments[0].click();", option)