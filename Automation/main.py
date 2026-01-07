from dotenv import load_dotenv
from core.browser import Browser
from core.login import Login
from core.navigation import Navigation
from workflows.closure import ClosureWorkflow
from workflows.blockage import BlockageWorkflow
from core.api import fetch_dummy_data
from core.rejection import RejectionCollector
import os

load_dotenv(override=True)

BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/dummy/")

driver = Browser.create()
rejections = RejectionCollector()

try:
    # ---------- LOGIN ----------
    Login(
        driver,
        os.getenv("odin_url"),
        os.getenv("username"),
        os.getenv("password")
    ).execute()

    # ---------- NAVIGATION ----------
    nav = Navigation(driver)
    nav.project()
    nav.layer_build()

    # ---------- FETCH DATA  ----------
    data = fetch_dummy_data(base_url=BASE_URL)

    if not data:
        print("No data received from API")

    # ---------- PROCESS IN EXACT API ORDER ----------
    for row in data:
        kind = row.get("kind")

        if kind == "closure":
            ClosureWorkflow(
                driver,
                rows=[row],             
                root_folder="Closure",
                rejections=rejections
            ).run()

        elif kind == "blockage":
            BlockageWorkflow(
                driver,
                rows=[row],              
                root_folder="Blockage",
                rejections=rejections
            ).run()

        else:
            rejections.add(
                row.get("Feature ID"),
                row.get("code"),
                f"Unknown kind: {kind}"
            )

    # ---------- PRINT REJECTIONS ----------
    rejections.print_all()
 
finally:
    driver.cleanup()
