import os

class BaseWorkflow:
    def __init__(self, driver, rows, root_folder):
        self.driver = driver
        self.rows = rows
        self.root_folder = root_folder

    def get_feature_folder(self, row):
        try:
            path = os.path.join(
                self.root_folder,
                f"{row['Assessor']} - {row['Polygon Type']} {row['Town']} {row['Contractor AFP ref']}",
                row["code"],
                str(row["Feature ID"])
            )
            os.makedirs(path, exist_ok=True)
            return path
        except OSError as e:
            print(f"[BLOCKER] Invalid download path:{path}")
            print(f"[BLOCKER] OS error : {e}")
            return None