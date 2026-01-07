import os
import time
import requests
from core.utils import convert_pdf_to_images, convert_pptx_to_images
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from variables import (
    POWER_BLOCK, POWER_HEADER, POWER_IMAGES,
    CARDS_PATH, DOC_PATH, DOWNLOAD_PATH,SHOW_MORE_MEDIA_BTN,MEDIA_CARDS,MEDIA_IMAGE,MEDIA_DROPDOWN_BTN,MEDIA_DROPDOWN_LINKS
    
)
from .base_media import BaseMedia


class ClosureMedia(BaseMedia):

    def download_power_meter_images(self, feature_id, excel_folder, code_value):
        wait = WebDriverWait(self.driver, 25)

        try:
            power_block = wait.until(EC.presence_of_element_located((By.XPATH, POWER_BLOCK)))
        except:
            return

        header = power_block.find_element(By.XPATH, POWER_HEADER)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", header)
        time.sleep(1)

        if "ant-collapse-item-active" not in power_block.get_attribute("class"):
            self.driver.execute_script("arguments[0].click();", header)
            time.sleep(1)

        images = power_block.find_elements(By.XPATH, POWER_IMAGES)

        count = 1
        for img in images:
            src = img.get_attribute("src")
            if not src:
                continue

            try:
                r = requests.get(src, timeout=20)
                r.raise_for_status()
            except:
                continue

            file_path = os.path.join(excel_folder, f"{code_value}_{feature_id}_{count}.jpg")
            with open(file_path, "wb") as f:
                f.write(r.content)

            count += 1

    ALLOWED_DOC_EXTS = {".pdf", ".pptx"}

    def download_closure_media(self, feature_id, excel_folder, code_value):
        driver = self.driver
        os.makedirs(excel_folder, exist_ok=True)

        try:
            show_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, SHOW_MORE_MEDIA_BTN)
                )
            )
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(1)
        except:
            pass

        try:
            cards = WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, MEDIA_CARDS)
                )
            )
        except TimeoutException:
            return

        seen_urls = set()
        counter = 1

        for card in cards:

            try:
                img = card.find_element(By.XPATH, MEDIA_IMAGE)
                src = img.get_attribute("src")

                if src and "base64" not in src and src not in seen_urls:
                    seen_urls.add(src)

                    try:
                        r = requests.get(src, timeout=20)
                        r.raise_for_status()
                    except:
                        continue

                    img_path = os.path.join(
                        excel_folder,
                        f"{code_value}_{feature_id}_{counter}.jpg"
                    )

                    with open(img_path, "wb") as f:
                        f.write(r.content)

                    counter += 1
                    continue

            except NoSuchElementException:
                pass

            try:
                dropdown_btn = card.find_element(
                    By.XPATH, MEDIA_DROPDOWN_BTN
                )

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    dropdown_btn
                )
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", dropdown_btn)
                time.sleep(0.5)

                links = driver.find_elements(
                    By.XPATH,MEDIA_DROPDOWN_LINKS
                )

                for link in links:
                    file_url = link.get_attribute("href")
                    if not file_url or file_url in seen_urls:
                        continue

                    seen_urls.add(file_url)

                    try:
                        r = requests.get(file_url, timeout=30)
                        r.raise_for_status()
                    except:
                        continue

                    content = r.content
                    content_type = r.headers.get("Content-Type", "").lower()

                    is_pdf = content.startswith(b"%PDF-") or "application/pdf" in content_type
                    is_pptx = (
                        "presentation" in content_type
                        or file_url.lower().endswith(".pptx")
                    )

                    if not is_pdf and not is_pptx:
                        continue

                    ext = ".pdf" if is_pdf else ".pptx"

                    file_path = os.path.join(
                        excel_folder,
                        f"{code_value}_{feature_id}_{counter}{ext}"
                    )

                    with open(file_path, "wb") as f:
                        f.write(content)

                    if is_pdf:
                        convert_pdf_to_images(
                            pdf_path=file_path,
                            output_dir=excel_folder,
                            base_name=f"{code_value}_{feature_id}_{counter}"
                        )

                    elif is_pptx:
                        try:
                            convert_pptx_to_images(
                                pptx_path=file_path,
                                output_dir=excel_folder,
                                base_name=f"{code_value}_{feature_id}_{counter}"
                            )
                        except:
                            pass

                    counter += 1

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            except (NoSuchElementException, TimeoutException):
                pass

    def download_all_media(self, feature_id, excel_folder, code_value):
        return self.download_closure_media(feature_id, excel_folder, code_value)
