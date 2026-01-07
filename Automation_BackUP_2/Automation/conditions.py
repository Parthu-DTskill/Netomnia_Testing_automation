from datetime import datetime
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from core.utils import scroll_drawer_until_visible, get_text_or_empty
from variables import BUILD_STATUS,SHOW_MORE_BTN, SIEBEL_REF_VALUE, WHEREABOUTS_VALUE



def validate_build_status(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)

    element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, BUILD_STATUS)
    ))

    raw_text = element.text.strip()
    # print("Raw Build Status Text:", raw_text)

    # Extract the first number using regex
    match = re.search(r"\d+", raw_text)
    if not match:
        return 0

    build_num = int(match.group())
    # print("Extracted Build Number:", build_num)

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
    print(f"Contractor: {contractor}")

    # Skip validation for mjq and gforce
    if contractor in ["mjq", "gforce"]:
        return True

    try:
        show_more = wait.until(
            EC.presence_of_element_located((By.XPATH, SHOW_MORE_BTN))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", show_more
        )
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", show_more)
        time.sleep(1)

        scroll_drawer_until_visible(driver, SIEBEL_REF_VALUE)
        scroll_drawer_until_visible(driver, WHEREABOUTS_VALUE)

        siebel_ref = get_text_or_empty(driver, SIEBEL_REF_VALUE)
        whereabouts = get_text_or_empty(driver, WHEREABOUTS_VALUE)

        print(f"Siebel Reference: '{siebel_ref}'")
        print(f"Whereabouts: '{whereabouts}'")

        if not siebel_ref or not whereabouts:
            print("Rejected → Missing Siebel Reference or Whereabouts")
            driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            return False

        return True

    except Exception as e:
        print("Siebel/Whereabouts validation failed:", e)
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        return False

# def validate_feature_date(driver, timeout=10):

#     wait = WebDriverWait(driver, timeout)

#     # date shown inside <span class="ant-typography">
#     date_element = wait.until(
#         EC.visibility_of_element_located(
#             (By.XPATH, "/html/body/div[7]/div/div[3]/div/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/span")
#         )
#     )

#     date_text = date_element.text.strip()
#     print("UI Date Found:", date_text)

#     try:
#         feature_date = datetime.strptime(date_text, "%d/%m/%Y")
#     except:
#         raise ValueError(f"Invalid date format from UI: {date_text}")

#     min_date = datetime(2023, 7, 31)
#     return feature_date >= min_date, date_text
def validate_feature_kind(row, expected_kind):
    """
    Validates whether the feature belongs to the expected workflow type.
    """
    actual_kind = row.get("kind")

    if actual_kind != expected_kind:
        return False, actual_kind

    return True, actual_kind
