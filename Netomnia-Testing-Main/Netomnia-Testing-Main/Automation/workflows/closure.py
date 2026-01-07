import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.api import fetch_dummy_data
from variables import (
    FEATURES_TAB,
    ABS_XPATH,
    CLOSURE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
)

from conditions import validate_build_status
from media.closure_media import ClosureMedia
from .base_workflow import BaseWorkflow


class ClosureWorkflow(BaseWorkflow):

    def run(self):
        media = ClosureMedia(self.driver)

        # with open(self.json_path, "r") as f:
        #     rows = json.load(f)
        

        rows = self.rows 

        wait = WebDriverWait(self.driver, 20)

        # self.select_feature_type(CLOSURE_OPTION)


        # FEATURES TAB
        features_tab = wait.until(
            EC.presence_of_element_located((By.XPATH, FEATURES_TAB))
        )
        self.driver.execute_script("arguments[0].click();", features_tab)

        

        # DROPDOWN 
        dropdown_panel = wait.until(EC.presence_of_element_located((By.XPATH, ABS_XPATH)))
        dropdown_panel.click()

        time.sleep(1)

        # CLOSURE OPTION
        option = wait.until(
            EC.presence_of_element_located((By.XPATH, CLOSURE_OPTION))
        )
        self.driver.execute_script("arguments[0].click();", option)
          

        # PROCESS FEATURES
        for row in rows:
            feature_id = int(row["Feature ID"])
            code = row["code"]
            folder = self.get_feature_folder(row)

            field = wait.until(
                EC.visibility_of_element_located((By.XPATH, FEATURE_ID_INPUT))
            )
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(Keys.DELETE)
            field.send_keys(str(feature_id))
            field.send_keys(Keys.ENTER)

            time.sleep(2)

            eye = wait.until(
                EC.presence_of_element_located((By.XPATH, EYE_BUTTON))
            )
            self.driver.execute_script("arguments[0].click();", eye)

            wait.until(
                EC.visibility_of_element_located((By.XPATH, BUILD_STATUS))
            )

            if validate_build_status(self.driver) < 7:
                self.rejections.add(feature_id,code,"Build status < 7")
                self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                continue

            if code == "TST003":
                media.download_power_meter_images(feature_id, folder, code)
            else:
                media.download_closure_media(feature_id, folder, code)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)
