import os

from core.pdf_image_extract import extract_images_from_pdf
from core.image_dedupe import remove_duplicates
from core.image_compress import compress_and_save_images


def process_pdf_media(pdf_path: str, feature_folder: str):
    """
    End-to-end PDF media pipeline:
    PDF → extract images → dedupe → compress
    """

    raw_dir = os.path.join(feature_folder, "raw_images")
    unique_dir = os.path.join(feature_folder, "unique_images")
    final_dir = os.path.join(feature_folder, "compressed_images")

    # Ensure folders exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(unique_dir, exist_ok=True)
    os.makedirs(final_dir, exist_ok=True)

    # 1️⃣ Extract images from PDF (PyMuPDF)
    extracted = extract_images_from_pdf(
        pdf_path=pdf_path,
        output_dir=raw_dir,
        base_name="img"
    )

    if not extracted:
        print(f"[INFO] No images found in PDF: {pdf_path}")
        return []

    # 2️⃣ Remove duplicates
    remove_duplicates(raw_dir, unique_dir)

    # 3️⃣ Compress images
    compressed_files, _ = compress_and_save_images(
        input_folder=unique_dir,
        output_folder=final_dir,
        max_size_kb=300,
        max_workers=4
    )

    return compressed_files
