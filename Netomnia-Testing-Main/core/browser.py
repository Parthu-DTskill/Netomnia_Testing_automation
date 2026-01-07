import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Browser:
    @staticmethod
    def create(headless=False):
        options = Options()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-popup-blocking")

        if headless:
            options.add_argument("--headless=new")

        profile_dir = tempfile.mkdtemp(prefix="chrome_profile_")
        options.add_argument(f"--user-data-dir={profile_dir}")

        driver = webdriver.Chrome(options=options)

        def cleanup():
            try:
                driver.quit()
            finally:
                shutil.rmtree(profile_dir, ignore_errors=True)

        driver.cleanup = cleanup
        return driver