import os
import json

# Load JSON data from a file

def load_json_data(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data]

    return data

def collect_feature_outputs(output_paths):
    """
    Returns final folders to report:
    - Images → feature folder
    - PDF/PPTX → compressed folder
    """
    collected = set()

    for path in output_paths:
        lower = path.lower()

        # PDF / PPTX
        if lower.endswith(".pdf") or lower.endswith(".pptx"):
            base_name = os.path.splitext(os.path.basename(path))[0]
            feature_dir = os.path.dirname(path)

            compressed_dir = os.path.join(
                feature_dir,
                base_name,
                "compressed"
            )
            collected.add(compressed_dir)

        # Images
        else:
            collected.add(os.path.dirname(path))

    return sorted(collected)