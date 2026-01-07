import shutil
import time,os,subprocess,tempfile
from helper import safe_rmtree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from selenium.common.exceptions import TimeoutException

def get_text_or_empty(driver, xpath, timeout=10):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
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
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", cards[-1]
        )
        time.sleep(0.6)
    return cards

def scroll_drawer_until_visible(driver, xpath, timeout=12):
    end_time = time.time() + timeout

    drawer = driver.find_element(By.CSS_SELECTOR, ".ant-drawer-body")

    while time.time() < end_time:
        try:
            el = driver.find_element(By.XPATH, xpath)

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
            time.sleep(0.5)

            if el.is_displayed():
                return el
        except:
            pass

        # smooth incremental scroll
        driver.execute_script(
            "arguments[0].scrollTop += 250;", drawer
        )
        time.sleep(0.4)

    raise TimeoutException(f"Element not visible: {xpath}")

def safe_scroll_into_view(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", element
    )
    time.sleep(0.3)

def convert_pdf_to_images(pdf_path, output_dir, base_name, dpi=300):
    os.makedirs(output_dir, exist_ok=True)
    poppler_path = os.environ.get("POPPLER_PATH")  


    try:
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            fmt="jpeg",
            poppler_path=poppler_path if poppler_path else None,
        )
    except PDFInfoNotInstalledError:
        print("[WARN] Poppler not installed")
        return []
    except Exception as e:
        print(f"[WARN] PDF conversion failed: {e}")
        return []

    paths = []
    for i, img in enumerate(images, 1):
        path = os.path.join(output_dir, f"{base_name}_page_{i}.jpg")
        img.save(path, "JPEG")
        paths.append(path)

    return paths


SOFFICE_PATH = os.environ["LIBREOFFICE_PATH"]


def convert_pptx_to_images(pptx_path, output_dir, base_name, dpi=150):
    if not os.path.isfile(pptx_path):
        raise FileNotFoundError(pptx_path)

    work_dir = tempfile.mkdtemp(prefix="libreoffice_work_")
    profile_dir = tempfile.mkdtemp(prefix="libreoffice_profile_")

    env = os.environ.copy()
    env["TMP"] = work_dir
    env["TEMP"] = work_dir

    try:
        subprocess.run(
            [
                SOFFICE_PATH,
                "--headless",
                "--invisible",
                "--nologo",
                "--nolockcheck",
                "--nodefault",
                f"-env:UserInstallation=file:///{profile_dir.replace(os.sep, '/')}",
                "--convert-to",
                "pdf",
                "--outdir",
                work_dir,
                pptx_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            env=env,
        )

        pdf_path = os.path.join(
            work_dir,
            os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
        )

        if not os.path.isfile(pdf_path):
            print(f"[WARN] LibreOffice did not generate PDF for: {pptx_path}")
            return []

        return convert_pdf_to_images(
            pdf_path=pdf_path,
            output_dir=output_dir,
            base_name=base_name,
            dpi=dpi,
        )

    finally:
        safe_rmtree(work_dir)
        safe_rmtree(profile_dir)
