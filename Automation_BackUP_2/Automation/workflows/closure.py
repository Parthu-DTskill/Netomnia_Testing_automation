import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from variables import (
    FEATURES_TAB,
    ABS_XPATH,
    CLOSURE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
    SUPPORTED_CODES,
)

from conditions import validate_build_status
from media.closure_media import ClosureMedia
from .base_workflow import BaseWorkflow


class ClosureWorkflow(BaseWorkflow):

    def run(self):
        media = ClosureMedia(self.driver)
        rows = self.rows
        wait = WebDriverWait(self.driver, 20)

        # ---------- RESET UI ONCE ----------
        features_tab = wait.until(
            EC.presence_of_element_located((By.XPATH, FEATURES_TAB))
        )
        self.driver.execute_script("arguments[0].click();", features_tab)

        dropdown_panel = wait.until(
            EC.presence_of_element_located((By.XPATH, ABS_XPATH))
        )
        dropdown_panel.click()

        time.sleep(1)

        option = wait.until(
            EC.presence_of_element_located((By.XPATH, CLOSURE_OPTION))
        )
        self.driver.execute_script("arguments[0].click();", option)

        # ---------- PROCESS FEATURES ----------
        for row in rows:
            feature_id = int(row["Feature ID"])
            kind = row.get("kind")
            code = row.get("code")

            # ---------- TYPE CHECK ----------
            if kind != "closure":
                print(
                    f"Skipped Feature ID {feature_id}: "
                    f"feature type '{kind}' is not valid for Closure workflow."
                )
                continue

            # ---------- CODE CHECK  ----------
            if code not in SUPPORTED_CODES:
                print(
                    f"Skipped Feature ID {feature_id}: "
                    f"code '{code}' is not supported."
                )
                continue

            folder = self.get_feature_folder(row)

            # ---------- SEARCH FEATURE ----------
            field = wait.until(
                EC.visibility_of_element_located((By.XPATH, FEATURE_ID_INPUT))
            )
            field.send_keys(Keys.CONTROL, "a")
            field.send_keys(Keys.DELETE)
            field.send_keys(str(feature_id))
            field.send_keys(Keys.ENTER)

            time.sleep(2)

            # ---------- FEATURE EXISTS CHECK  ----------
            try:
                eye = wait.until(
                    EC.presence_of_element_located((By.XPATH, EYE_BUTTON))
                )
            except TimeoutException:
                print(
                    f"Skipped Feature ID {feature_id}: "
                    f"feature not found in UI."
                )
                continue

            self.driver.execute_script("arguments[0].click();", eye)

            wait.until(
                EC.visibility_of_element_located((By.XPATH, BUILD_STATUS))
            )

            # ---------- BUILD STATUS CHECK ----------
            if validate_build_status(self.driver) < 7:
                self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                continue

            # ---------- DOWNLOAD ----------
            if code == "TST003":
                media.download_power_meter_images(feature_id, folder, code)
            else:
                media.download_closure_media(feature_id, folder, code)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)
