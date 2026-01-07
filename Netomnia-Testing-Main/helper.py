import os, shutil,time


def get_latest_techm_file():
    base_folder = os.path.dirname(__file__)
    upload_folder = os.path.join(base_folder, "upload")

    if not os.path.exists(upload_folder):
        raise FileNotFoundError(
            f"Upload folder does not exist: {upload_folder}")

    excel_files = [
        os.path.join(upload_folder, f)
        for f in os.listdir(upload_folder)
        if f.startswith("TechM") and f.endswith(".xlsx")
    ]

    if not excel_files:
        raise FileNotFoundError(
            f"No TechM Excel files found in: {upload_folder}")

    # print(f"Found {len(excel_files)} TechM files:")
    for f in excel_files:
        print("  ", os.path.basename(f))

    return excel_files

def safe_rmtree(path, retries=5, delay=0.5):
    for _ in range(retries):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
            return
        except PermissionError:
            time.sleep(delay)
    print(f"[WARN] Could not delete locked directory: {path}")