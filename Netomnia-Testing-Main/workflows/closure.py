import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_workflow import BaseWorkflow
from media.closure_media import ClosureMedia
from conditions import validate_build_status
from variables import (
    FEATURE_ID_INVALID,
    CLOSURE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
)




class ClosureWorkflow(BaseWorkflow):

    def run(self):

        media = ClosureMedia(self.driver)
        self.output_paths = []
        self.outputs = {}
        tst002_executed = False
        rows = self.rows 

        self.open_feature_type(CLOSURE_OPTION)
        
        wait = WebDriverWait(self.driver, 20)
          
        for row in rows:

            paths = None 
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


            # TST003

            if code == "TST003":

                paths = media.download_power_meter_images(feature_id, folder, code)

                if not paths:
                    self.rejections.add(feature_id, code,"No Power Meter images found")
                    continue

            # TST002

            elif code == "TST002":

                tst002_executed = True

                self.outputs.setdefault("closure", {})
                self.outputs["closure"].setdefault("TST002", {})
                self.outputs["closure"]["TST002"][feature_id] = "NOK"
                
                quantity = int(row.get("quantity", 0))

                if quantity <= 1:
                    self.rejections.add(feature_id, code,"Quantity must be greater than 1 for TST002")
                    continue

                pdf_count = media.count_otdr_pdfs_ui()

                if pdf_count == 0:
                    self.rejections.add(feature_id, code,"No OTDR PDF evidence found")
                    continue

                if pdf_count > quantity:
                    self.rejections.add(feature_id, code,"Under-claim: OTDR PDF count exceeds declared quantity")
                    continue

                if pdf_count < quantity:
                    self.rejections.add(feature_id, code,"Over-claim: OTDR PDF count less than declared quantity")
                    continue   

                result = media.latest_otdr_pdf_is_iolm_ui()

                if result is False:
                    self.rejections.add(feature_id, code, "Latest OTDR PDF is not an iOLM report")

                elif result is None:
                    print("[INFO] iOLM check skipped due to UI instability") 

                self.outputs["closure"]["TST002"][feature_id] = "OK"
 
            # OTHER CODES
            else:
                paths = media.download_closure_media(feature_id, folder, code)

            if paths:
                if isinstance(paths, list):
                    self.output_paths.extend(paths)
                else:
                    self.output_paths.append(paths)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)

        if not tst002_executed:
            self.outputs.pop("closure", None)