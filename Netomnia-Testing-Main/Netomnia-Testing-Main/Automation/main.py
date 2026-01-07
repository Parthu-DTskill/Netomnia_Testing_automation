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
    Login(
        driver,
        os.getenv("odin_url"),
        os.getenv("username"),
        os.getenv("password")
    ).execute()

    nav = Navigation(driver)
    nav.project()
    nav.layer_build()

    data = fetch_dummy_data(
        base_url=BASE_URL,
        grouped=True
    )

    # data = fetch_dummy_data(base_url=BASE_URL)

    # for row in data:
    #     kind = row.get("kind")

    #     if kind == "closure":
    #         ClosureWorkflow(
    #             driver,
    #             rows=[row],     # process ONE row
    #             root_folder="Closure",
    #             rejections=rejections
    #         ).run()

    #     elif kind == "blockage":
    #         BlockageWorkflow(
    #             driver,
    #             rows=[row],
    #             root_folder="Blockage",
    #             rejections=rejections
    #         ).run()

    #     else:
    #         rejections.add(
    #             row.get("Feature ID"),
    #             row.get("code"),
    #             f"Unknown kind: {kind}"
    #         )


    closures = data.get("closures") or []
    blockages = data.get("blockages") or []


    if not closures and not blockages:
        print("No Closure or Blockage data received from API")

    if closures:
        ClosureWorkflow(driver,rows=closures,root_folder="Closure",rejections=rejections).run()

    if blockages:
        BlockageWorkflow(driver,rows=blockages,root_folder="Blockage",rejections=rejections).run()

    # ClosureWorkflow(driver, rows=closures, root_folder="Closure", rejections=rejections).run()

    # # print("\n" + "=" * 50 + "\n")

    # BlockageWorkflow(driver, rows=blockages, root_folder="Blockage",  rejections=rejections).run()

    rejections.print_all()

finally:
    driver.cleanup()