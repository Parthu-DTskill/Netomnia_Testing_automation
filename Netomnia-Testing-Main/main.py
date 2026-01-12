import os
import json
from helper import load_json_data, collect_feature_outputs
from variables import BLOCKAGE_CODES, CLOSURE_CODES
from dotenv import load_dotenv
from core.browser import Browser
from core.login import Login
from core.navigation import Navigation
from workflows.closure import ClosureWorkflow
from workflows.blockage import BlockageWorkflow
from core.api import fetch_dummy_data
from core.rejection import RejectionCollector


load_dotenv(override=True)

#BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/dummy/")

JSON_PATH = "data/blockage_1.json"

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

    rows = load_json_data(JSON_PATH)

    closures = []
    blockages = []
    final_result = {"outputs": {},"rejections": []}

    for row in rows:
        feature_id = row.get("Feature ID")
        code = row.get("code")

        if not feature_id or not code:
            rejections.add(feature_id, code, "Missing Feature ID or code")
            continue

        if code in CLOSURE_CODES:
            closures.append(row)

        elif code in BLOCKAGE_CODES:
            blockages.append(row)

        else:
            rejections.add(feature_id, code, f"Unsupported code: {code}")



    # Closure
    if closures:
        cw = ClosureWorkflow(driver,rows=closures,root_folder="Closure",rejections=rejections)
        cw.run()
        
        if cw.output_paths:
            final_result["outputs"]["Closure"] = collect_feature_outputs(cw.output_paths)

    # Blockage
    if blockages:
        bw = BlockageWorkflow(driver,rows=blockages,root_folder="Blockage",rejections=rejections)
        bw.run()

        if bw.output_paths:
            final_result["outputs"]["Blockage"] = collect_feature_outputs(bw.output_paths)

    # Rejections
    final_result["rejections"] = rejections.to_list()

    # PRINT TO TERMINAL
    print("\n===== FINAL OUTPUT =====")
    print(json.dumps(final_result, indent=4))

    # Save to file

    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=4)
        
finally:
    driver.cleanup()