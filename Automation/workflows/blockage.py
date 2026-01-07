import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.utils import scroll_drawer_until_visible
from core.utils import get_text_or_empty
from core.api import fetch_dummy_data
from variables import (
    FEATURE_ID_INVALID,
    FEATURES_TAB,
    SELECT_DROPDOWN_SELECTOR,
    BLOCKAGE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
    ABS_XPATH,
)

from conditions import validate_build_status, validate_siebel_and_whereabouts
from media.closure_media import ClosureMedia
from .base_workflow import BaseWorkflow


class BlockageWorkflow(BaseWorkflow):

    def run(self):
        media = ClosureMedia(self.driver)

        # with open(self.json_path, "r") as f:
        #     rows = json.load(f)
        rows = self.rows

        if isinstance(rows, dict):
            rows = [rows]

        wait = WebDriverWait(self.driver, 20)

        # features_tab = wait.until(
        #     EC.presence_of_element_located((By.XPATH, FEATURES_TAB))
        # )
        # self.driver.execute_script("arguments[0].click();", features_tab)


            # dropdown_panel = wait.until(EC.presence_of_element_located((By.XPATH, ABS_XPATH)))
            # dropdown_panel.click()


            # time.sleep(1)

            # option = wait.until(
            #     EC.presence_of_element_located((By.XPATH, BLOCKAGE_OPTION))
            # )
            # self.driver.execute_script("arguments[0].click();", option)

        self.select_feature_type(BLOCKAGE_OPTION)
        
        for row in rows:
            feature_id = int(row["Feature ID"])
            code = row["code"]
            folder = self.get_feature_folder(row)

            try:
                field = wait.until(EC.visibility_of_element_located((By.XPATH, FEATURE_ID_INPUT)))
                field.send_keys(Keys.CONTROL, "a")
                field.send_keys(Keys.DELETE)
                field.send_keys(str(feature_id))
                field.send_keys(Keys.ENTER)
            except Exception:
                self.rejections.add(feature_id,code,"Feature ID input failed")
                continue


            # field = wait.until(
            #     EC.visibility_of_element_located((By.XPATH, FEATURE_ID_INPUT))
            # )
            # field.send_keys(Keys.CONTROL, "a")
            # field.send_keys(Keys.DELETE)
            # field.send_keys(str(feature_id))
            # field.send_keys(Keys.ENTER)
            
            time.sleep(2)

            if self.driver.find_elements(By.XPATH, FEATURE_ID_INVALID):
                self.rejections.add(feature_id,code,"Invalid Feature ID (No data found)")
                continue

            eye = wait.until(EC.presence_of_element_located((By.XPATH, EYE_BUTTON)))
            self.driver.execute_script("arguments[0].click();", eye)


            wait.until(
                EC.visibility_of_element_located((By.XPATH, BUILD_STATUS))
            )

            if validate_build_status(self.driver) < 7:
                self.rejections.add(feature_id,code,"Build status < 7")
                self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                continue

            if not validate_siebel_and_whereabouts(self.driver, row, wait):
                self.rejections.add(feature_id,code,"Missing or invalid Siebel / Whereabouts")
                continue      

            media.download_closure_media(feature_id, folder, code)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)