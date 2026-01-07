# from dotenv import load_dotenv
# from core.browser import Browser
# from core.login import Login
# from core.navigation import Navigation
# from workflows.closure import ClosureWorkflow
# from workflows.blockage import BlockageWorkflow
# from core.api import fetch_dummy_data
# import os

# load_dotenv(override=True)

# BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/dummy/")

# def main():
#     driver = Browser.create()

#     try:
#         Login(
#             driver,
#             os.getenv("odin_url"),
#             os.getenv("username"),
#             os.getenv("password")
#         ).execute()

#         nav = Navigation(driver)
#         nav.project()
#         nav.layer_build()

#         data = fetch_dummy_data(
#             base_url=BASE_URL,
#             grouped=True
#         )

#         closures = data.get("closures", [])
#         blockages = data.get("blockages", [])

#         ClosureWorkflow(driver, rows=closures, root_folder="Closure").run()

#         print("\n" + "=" * 50 + "\n")

#         BlockageWorkflow(driver, rows=blockages, root_folder="Blockage").run()

#     finally:
#         driver.cleanup()

# if __name__ == "__main__":
#     main()
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

    # Fetch a flat list to preserve ordering from the API. If the API returns grouped data for
    # backward compatibility, flatten it while preserving original ordering within each group.
    data = fetch_dummy_data(base_url=BASE_URL)

    # If grouped format is returned, convert to flat list preserving sequence within groups
    if isinstance(data, dict) and ("closures" in data or "blockages" in data):
        flattened = []
        # keep the same ordering within each group, and append groups in closures->blockages order
        for kind in ("closures", "blockages"):
            items = data.get(kind) or []
            for row in items:
                # ensure 'kind' is present so workflows can filter
                row["kind"] = "closure" if kind == "closures" else "blockage"
                flattened.append(row)
        data = flattened

    # If API already returned an ordered list, process it in sequence and dispatch per-row
    if isinstance(data, list):
        for row in data:
            kind = row.get("kind")
            if kind == "closure":
                ClosureWorkflow(
                    driver,
                    rows=[row],
                    root_folder="Closure",
                    rejections=rejections,
                ).run()
            elif kind == "blockage":
                BlockageWorkflow(
                    driver,
                    rows=[row],
                    root_folder="Blockage",
                    rejections=rejections,
                ).run()
            else:
                rejections.add(
                    row.get("Feature ID"), row.get("code"), f"Unknown kind: {kind}"
                )
    else:
        print("Unexpected API response format; no rows to process")

    rejections.print_all()

finally:
    driver.cleanup()