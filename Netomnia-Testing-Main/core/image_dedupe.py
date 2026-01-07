import os
import shutil
import hashlib
from PIL import Image
import imagehash
from itertools import combinations

PHASH_THRESHOLD = 8


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def remove_duplicates(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    # ---- Exact duplicates (MD5)
    hash_map = {}
    for f in files:
        h = md5(os.path.join(input_dir, f))
        hash_map.setdefault(h, []).append(f)

    unique_files = [group[0] for group in hash_map.values()]

    # ---- Near duplicates (pHash)
    phashes = {}
    final_files = []

    for f in unique_files:
        img = Image.open(os.path.join(input_dir, f)).convert("RGB")
        phashes[f] = imagehash.phash(img)

    for f in unique_files:
        if all(phashes[f] - phashes[g] > PHASH_THRESHOLD for g in final_files):
            final_files.append(f)

    # ---- Copy unique images
    for f in final_files:
        shutil.copy(
            os.path.join(input_dir, f),
            os.path.join(output_dir, f)
        )

    return final_files
