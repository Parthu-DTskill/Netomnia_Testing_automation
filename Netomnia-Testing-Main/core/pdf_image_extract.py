import os
import fitz  # PyMuPDF
import io
from PIL import Image


def extract_images_from_pdf(pdf_path, output_dir, base_name="img"):
    os.makedirs(output_dir, exist_ok=True)
    extracted_files = []

    doc = fitz.open(pdf_path)
    counter = 1

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        images = page.get_images(full=True)

        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image.get("ext", "png")

            image = Image.open(io.BytesIO(image_bytes))
            filename = f"{base_name}_{counter}.{image_ext}"
            path = os.path.join(output_dir, filename)

            image.save(path)
            extracted_files.append(path)
            counter += 1

    doc.close()
    return extracted_files
