import io
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    success: bool
    input_path: str
    output_path: Optional[str]
    original_size_kb: float
    compressed_size_kb: Optional[float]
    error: Optional[str]


def compress_and_save_images(
    input_folder: str,
    output_folder: str,
    max_size_kb: int = 300,
    max_workers: Optional[int] = None,
) -> Tuple[List[str], List[CompressionResult]]:
    """
    Compress all images in input_folder and save to output_folder.
    """

    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    output_path.mkdir(parents=True, exist_ok=True)

    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
    image_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in valid_exts
    ]

    results: List[CompressionResult] = []
    successful_files: List[str] = []

    if max_workers and max_workers > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _compress_single_image,
                    img,
                    output_path / f"{i}.jpg",
                    max_size_kb,
                ): img
                for i, img in enumerate(image_files, 1)
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if result.success:
                    successful_files.append(result.output_path)

    else:
        for i, img in enumerate(image_files, 1):
            result = _compress_single_image(
                img,
                output_path / f"{i}.jpg",
                max_size_kb
            )
            results.append(result)
            if result.success:
                successful_files.append(result.output_path)

    return successful_files, results


def _compress_single_image(
    image_path: Path,
    output_path: Path,
    max_size_kb: int,
) -> CompressionResult:
    try:
        original_bytes = image_path.read_bytes()
        original_size = len(original_bytes) / 1024

        compressed_bytes = _compress_image_bytes(
            original_bytes,
            max_size_kb
        )

        compressed_size = len(compressed_bytes) / 1024
        output_path.write_bytes(compressed_bytes)

        return CompressionResult(
            success=True,
            input_path=str(image_path),
            output_path=str(output_path),
            original_size_kb=original_size,
            compressed_size_kb=compressed_size,
            error=None,
        )

    except Exception as e:
        return CompressionResult(
            success=False,
            input_path=str(image_path),
            output_path=None,
            original_size_kb=0,
            compressed_size_kb=None,
            error=str(e),
        )


def _compress_image_bytes(image_bytes: bytes, max_size_kb: int) -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    for quality in [85, 75, 65, 55, 45, 35]:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        if len(buf.getvalue()) / 1024 <= max_size_kb:
            return buf.getvalue()

    # fallback resize
    w, h = img.size
    img = img.resize((int(w * 0.5), int(h * 0.5)), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=30, optimize=True)
    return buf.getvalue()
