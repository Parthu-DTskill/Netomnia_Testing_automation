import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from variables import (
    FEATURES_TAB,
    SELECT_DROPDOWN_SELECTOR,
    BLOCKAGE_OPTION,
    FEATURE_ID_INPUT,
    EYE_BUTTON,
    BUILD_STATUS,
    SHOW_MORE_BTN,
    SUPPORTED_CODES,
    SIEBEL_REF_VALUE,         
    WHEREABOUTS_VALUE,
)

from conditions import validate_build_status
from media.closure_media import ClosureMedia
from .base_workflow import BaseWorkflow


class BlockageWorkflow(BaseWorkflow):

    def run(self):
        media = ClosureMedia(self.driver)
        rows = self.rows

        if isinstance(rows, dict):
            rows = [rows]

        wait = WebDriverWait(self.driver, 20)

        # ---------- RESET UI ONCE  ----------
        features_tab = wait.until(
            EC.presence_of_element_located((By.XPATH, FEATURES_TAB))
        )
        self.driver.execute_script("arguments[0].click();", features_tab)

        selector = wait.until(
            EC.presence_of_element_located((By.XPATH, SELECT_DROPDOWN_SELECTOR))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", selector
        )
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", selector)

        time.sleep(1)

        option = wait.until(
            EC.presence_of_element_located((By.XPATH, BLOCKAGE_OPTION))
        )
        self.driver.execute_script("arguments[0].click();", option)

        # ---------- PROCESS FEATURES ----------
        for row in rows:
            feature_id = int(row["Feature ID"])
            kind = row.get("kind")
            code = row.get("code")
            contractor = row.get("Contractor", "").lower().strip()

            # ---------- TYPE CHECK ----------
            if kind != "blockage":
                print(
                    f"Skipped Feature ID {feature_id}: "
                    f"feature type '{kind}' is not valid for Blockage workflow."
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

            # ---------- CONTRACTOR-SPECIFIC CHECK  ----------
            if contractor not in ("mjq", "gforce"):
                try:
                    siebel = wait.until(
                        EC.visibility_of_element_located((By.XPATH, SIEBEL_REF_VALUE))
                    )
                    whereabouts = wait.until(
                        EC.visibility_of_element_located((By.XPATH, WHEREABOUTS_VALUE))
                    )
                except TimeoutException:
                    print(
                        f"Skipped Feature ID {feature_id}: "
                        f"Siebel Reference / Whereabouts missing."
                    )
                    self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                    continue

            # ---------- SHOW MORE ----------
            try:
                show_more = wait.until(
                    EC.presence_of_element_located((By.XPATH, SHOW_MORE_BTN))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", show_more
                )
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", show_more)
                time.sleep(1)
            except:
                pass

            # ---------- DOWNLOAD ----------
            media.download_closure_media(feature_id, folder, code)

            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)
