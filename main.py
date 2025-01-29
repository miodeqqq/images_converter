import argparse
import logging
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from pathlib import Path
from time import time
from typing import Tuple

from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

register_heif_opener()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_image(task_args: Tuple[Path, Path, int, int]) -> None:
    """
    Process a single image: convert to JPG (if necessary), resize, and save.

    Args:
        task_args (tuple): (input_path, output_dir, quality_decrease, index)
    """

    input_path, output_dir, quality_decrease, index = task_args

    save_config = {
        "format": "JPEG",
        "quality": 100,
        "optimize": False,
    }

    output_path = output_dir / f"{index}_{input_path.stem}.jpg"

    try:
        with Image.open(fp=input_path) as img:
            if img.mode in ("RGBA", "P", "CMYK", "LA"):
                img = img.convert(mode="RGB")

            width, height = img.size

            if quality_decrease and quality_decrease > 0:
                scale_factor = 1 - quality_decrease / 100

                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)

                img = img.resize(
                    size=(new_width, new_height),
                    resample=Image.Resampling.LANCZOS,
                )

            img.save(fp=output_path, **save_config)
    except (OSError, IOError, Image.DecompressionBombError) as exc:
        logging.error(msg=f"Error processing {input_path}: {str(exc)}")


def convert_images(input_dir: str, quality_decrease: int) -> None:
    """
    Convert all images in a directory to JPG format and optionally resize them.

    Args:
        input_dir (str): Directory containing input images.
        quality_decrease (int): Percentage to reduce image size (0-100).
    """

    input_path = Path(input_dir)

    if not input_path.is_dir():
        raise ValueError(f"Input directory '{input_dir}' does not exist.")

    start_time = time()

    valid_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".heic",
        ".dng",
        ".bmp",
        ".tiff",
        ".gif",
    )

    image_files = [
        img_file
        for img_file in input_path.rglob(pattern="*")
        if img_file.is_file() and img_file.suffix.lower() in valid_extensions
    ]

    if not image_files:
        logging.warning(msg="No valid image files found in the directory.")
    else:
        total_images = len(image_files)

        logging.info(msg=f"Found {total_images} images to process.")

        output_dir = input_path / "_converted"
        output_dir.mkdir(exist_ok=True)

        tasks = [
            (img_file, output_dir, quality_decrease, index)
            for index, img_file in enumerate(image_files, start=1)
        ]

        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            list(
                tqdm(
                    iterable=executor.map(process_image, tasks, chunksize=10),
                    total=total_images,
                    desc=logging.info(msg="Processing images ..."),
                    file=sys.stdout,
                )
            )

        diff = time() - start_time

        logging.info(
            msg=f"Done in {diff:.2f} seconds. Images saved to '{output_dir}'."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert images to JPG format and optionally resize them."
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Path to the input directory containing images.",
    )

    parser.add_argument(
        "--quality",
        type=int,
        required=False,
        help="Percentage to reduce image size (0-100).",
    )

    args = parser.parse_args()

    convert_images(input_dir=args.input_dir, quality_decrease=args.quality)
