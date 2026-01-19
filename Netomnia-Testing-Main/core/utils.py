import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_text_or_empty(driver, xpath, timeout=10):
    try:
        el = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return el.text.strip()
    except:
        return ""


def scroll_and_collect_cards(driver, cards_xpath):
    last = -1
    while True:
        cards = driver.find_elements(By.XPATH, cards_xpath)
        if len(cards) == last:
            break
        last = len(cards)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cards[-1])
        time.sleep(0.6)
    return cards

def scroll_drawer_until_visible(driver, xpath, timeout=12):

    end_time = time.time() + timeout
    drawer = driver.find_element(By.CSS_SELECTOR, ".ant-drawer-body")

    while time.time() < end_time:
        try:
            el = driver.find_element(By.XPATH, xpath)

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)

            if el.is_displayed():
                return el
        except:
            pass

        driver.execute_script("arguments[0].scrollTop += 250;", drawer)
        time.sleep(0.4)

    raise TimeoutException(f"Element not visible: {xpath}")

def safe_scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.3)