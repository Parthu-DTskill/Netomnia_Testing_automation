import re
import time
from core.utils import scroll_drawer_until_visible, get_text_or_empty
from variables import BUILD_STATUS,SHOW_MORE_BTN, SIEBEL_REF_VALUE, WHEREABOUTS_VALUE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def validate_build_status(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)

    element = wait.until(EC.visibility_of_element_located((By.XPATH, BUILD_STATUS)))
    raw_text = element.text.strip()

    match = re.search(r"\d+", raw_text)
    if not match:
        return 0

    build_num = int(match.group())
    return build_num


def is_duplicate_row(row, df):
    polygon_id = int(row["Polygon ID"])
    feature_id = int(row["Feature ID"])
    code = row["code"]

    duplicates = df[
        (df["Polygon ID"] == polygon_id) &
        (df["Feature ID"] == feature_id) &
        (df["code"] == code)
    ]

    return len(duplicates) > 1


def validate_siebel_and_whereabouts(driver, row, wait):
    """
    Returns True if validation passes
    Returns False if feature should be rejected
    """

    contractor = row.get("Contractor", "").lower().strip()

    if contractor in ["mjq", "gforce"]:
        return True

    try:
        show_more = wait.until(EC.presence_of_element_located((By.XPATH, SHOW_MORE_BTN)))
        driver.execute_script( "arguments[0].scrollIntoView({block:'center'});", show_more)
        time.sleep(0.5)

        driver.execute_script("arguments[0].click();", show_more)
        time.sleep(1)

        scroll_drawer_until_visible(driver, SIEBEL_REF_VALUE)
        scroll_drawer_until_visible(driver, WHEREABOUTS_VALUE)

        siebel_ref = get_text_or_empty(driver, SIEBEL_REF_VALUE)
        whereabouts = get_text_or_empty(driver, WHEREABOUTS_VALUE)

        if not siebel_ref or not whereabouts:
            driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            return False

        return True

    except Exception as e:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        return False