from core.pdf_image_extract import extract_images_from_pdf
from core.image_dedupe import remove_duplicates
from core.image_compress import compress_and_save_images
from core.pptx_image_extract import extract_images_from_pptx
import os

def process_document(file_path, feature_folder, base_name):

    raw_dir = os.path.join(feature_folder, base_name, "raw")
    unique_dir = os.path.join(feature_folder, base_name, "unique")
    final_dir = os.path.join(feature_folder, base_name, "compressed")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(unique_dir, exist_ok=True)
    os.makedirs(final_dir, exist_ok=True)

    ext = os.path.splitext(file_path)[1].lower()

    extracted = []

    if ext == ".pdf":
        extracted = extract_images_from_pdf(
            pdf_path=file_path,
            output_dir=raw_dir,
            base_name=base_name,
        )

    elif ext == ".pptx":
        extracted = extract_images_from_pptx(
            pptx_path=file_path,
            output_dir=raw_dir,
            prefix=base_name,
        )

    else:
        return []


    if not extracted:
        print(f"[INFO] No images extracted from {file_path}")
        return []

    remove_duplicates(raw_dir, unique_dir)

    compressed_files, _ = compress_and_save_images(
        input_folder=unique_dir,
        output_folder=final_dir,
        max_size_kb=300,
        max_workers=4,
    )

    return compressed_files