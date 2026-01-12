import os
import time
import requests
#from core.utils import convert_pdf_to_images, convert_pptx_to_images
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from variables import (
    POWER_BLOCK, POWER_HEADER, POWER_IMAGES,
)
from core.pdf_image_extract import extract_images_from_pdf
from core.image_dedupe import remove_duplicates
from core.image_compress import compress_and_save_images
from .base_media import BaseMedia
from core.media_processor import process_document

class ClosureMedia(BaseMedia):

    def process_pdf_or_pptx(self, file_path, excel_folder, base_name):
        raw_dir = os.path.join(excel_folder, base_name, "raw")
        unique_dir = os.path.join(excel_folder, base_name, "unique")
        final_dir = os.path.join(excel_folder, base_name, "compressed")

        os.makedirs(raw_dir, exist_ok=True)
        os.makedirs(unique_dir, exist_ok=True)
        os.makedirs(final_dir, exist_ok=True)

        # Extract embedded images
        extracted = extract_images_from_pdf(
            pdf_path=file_path,
            output_dir=raw_dir,
            base_name=base_name
        )

        if not extracted:
            return []

        # Remove duplicates
        remove_duplicates(raw_dir, unique_dir)

        # Compress images
        compressed_files, _ = compress_and_save_images(
            input_folder=unique_dir,
            output_folder=final_dir,
            max_size_kb=300,
            max_workers=4
        )

        return compressed_files


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

            self.saved_paths.append(file_path)  # STORE PATH

            count += 1
    
        return self.saved_paths

    ALLOWED_DOC_EXTS = {".pdf", ".pptx"}

    def download_closure_media(self, feature_id, excel_folder, code_value):
        driver = self.driver
        os.makedirs(excel_folder, exist_ok=True)

        try:
            show_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[normalize-space()='Show more']]")
                )
            )
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(1)
        except:
            pass

        try:
            cards = WebDriverWait(driver, 8).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class,'filePreviewCard')]")
                )
            )
        except TimeoutException:
            return

        seen_urls = set()
        counter = 1

        for card in cards:

            try:
                img = card.find_element(By.XPATH, ".//img[contains(@class,'ant-image-img')]")
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

                    self.saved_paths.append(img_path)  # STORE PATH


                    counter += 1
                    continue

            except NoSuchElementException:
                pass

            try:
                dropdown_btn = card.find_element(
                    By.XPATH, ".//button[contains(@class,'ant-dropdown-trigger')]"
                )

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    dropdown_btn
                )
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", dropdown_btn)
                time.sleep(0.5)

                links = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]"
                    "//a[contains(@href,'http')]"
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

                    self.saved_paths.append(file_path)  # STORE PATH

                    process_document(
                        file_path=file_path,
                        feature_folder=excel_folder,
                        base_name=f"{code_value}_{feature_id}_{counter}",
                    )  

                    counter += 1

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            except (NoSuchElementException, TimeoutException):
                pass
        
        return self.saved_paths

    def download_all_media(self, feature_id, excel_folder, code_value):
        return self.download_closure_media(feature_id, excel_folder, code_value)
