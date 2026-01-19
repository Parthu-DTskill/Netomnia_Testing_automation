import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_workflow import BaseWorkflow
from media.closure_media import ClosureMedia
from conditions import validate_build_status, validate_siebel_and_whereabouts
from variables import (
    FEATURE_ID_INVALID,
    BLOCKAGE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
)


class BlockageWorkflow(BaseWorkflow):

    def run(self):

        media = ClosureMedia(self.driver)
        self.output_paths = []
        rows = self.rows

        if isinstance(rows, dict):
            rows = [rows]

        self.open_feature_type(BLOCKAGE_OPTION)

        wait = WebDriverWait(self.driver, 20)

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
           
            time.sleep(2)

            if self.driver.find_elements(By.XPATH, FEATURE_ID_INVALID):
                self.rejections.add(feature_id,code,"Invalid Feature ID (No data found)")
                continue

            eye = wait.until(EC.presence_of_element_located((By.XPATH, EYE_BUTTON)))
            self.driver.execute_script("arguments[0].click();", eye)

            wait.until(EC.visibility_of_element_located((By.XPATH, BUILD_STATUS)))

            if validate_build_status(self.driver) < 7:
                self.rejections.add(feature_id,code,"Build status < 7")
                self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                continue

            if not validate_siebel_and_whereabouts(self.driver, row, wait):
                self.rejections.add(feature_id,code,"Missing or invalid Siebel / Whereabouts")
                continue      

            paths = media.download_closure_media(feature_id, folder, code)
            
            if paths:
                if isinstance(paths, list):
                    self.output_paths.extend(paths)
                else:
                    self.output_paths.append(paths)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)