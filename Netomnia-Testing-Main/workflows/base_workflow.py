import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from variables import FEATURE_TYPE_DROPDOWN, FEATURES_PANEL, FEATURES_TAB, ABS_XPATH

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
    
    def select_feature_type(self, option_xpath):

        wait = WebDriverWait(self.driver, 20)

        # # Close any open drawer / dropdown / overlay
        # self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        # time.sleep(0.4)



        # Click FEATURES tab again (safe reset)
        features_tab = wait.until(
            EC.presence_of_element_located((By.XPATH, FEATURES_TAB))
        )
        self.driver.execute_script("arguments[0].click();", features_tab)
        time.sleep(1)


        # wait.until(
        # EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'ant-drawer-body')]")))

        # selector = wait.until(
        # EC.element_to_be_clickable((By.XPATH, FEATURE_TYPE_DROPDOWN)))
        # self.driver.execute_script("arguments[0].click();", selector)
        # time.sleep(0.4)

        # dropdown_panel = wait.until(EC.presence_of_element_located((By.XPATH, ABS_XPATH)))
        # dropdown_panel.click()
       

        # Select required option (closure / blockage)
        option = wait.until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.4)
