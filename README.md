# Images Converter

This Python script converts images in a specified directory to JPEG format, optionally resizing them based on a quality reduction percentage. 

It processes multiple images in parallel, utilizing all available system resources for efficiency. A progress bar is displayed to provide real-time updates.

---

## Features

- **Format Conversion**: Converts images to JPEG format, handling various input formats such as HEIC, PNG, TIFF, BMP, GIF, and more.
- **Resizing**: Optionally resizes images based on a quality reduction percentage (0-100%).
- **Parallel Processing**: Utilizes multiprocessing to process images simultaneously, maximizing system resources.
- **Progress Indicator**: Includes a real-time progress bar using `tqdm`.

---

## Prerequisites

- **For Docker**: 
  - Ensure Docker is installed on your system.
  - No need to manually install Python, dependencies, or libraries — everything runs in a Docker container.

---

## Usage with Docker

### 1. **Build the Docker Image**

To create a Docker image for the script run:
```bash
make build_image
```

### 2. **Run the Docker Container**

To process images using Docker:
```bash
docker run --rm -v /path/to/images:/input images_converter --input-dir /input --quality <quality-percentage>
```

Replace `/path/to/images` with the path to the directory containing your images. The script will create a `_converted` subdirectory within `/path/to/images` where the processed images will be saved.

### Example:
Convert all images in `/Users/username/Desktop/photos` with no resizing:
```bash
docker run --rm -v /Users/username/Desktop/photos:/input images_converter --input-dir /input --quality 0
```

---

## Usage with Python (Optional)

If you prefer to run the script without Docker, you can use the following steps:

### 1. **Install Python and Poetry**

- Python 3.12+
- Install Poetry:
  ```bash
  pip install poetry
  ```

### 2. **Set Up the Environment**

- Create a virtual environment and install dependencies:
  ```bash
  poetry env use python3.13
  poetry install -vvv --no-root
  ```

### 3. **Run the Script**

Run the script from the command line:
```bash
poetry run python main.py --input-dir <path-to-input-directory> --quality <quality-percentage>
```

---

## Arguments

- `--input-dir` (required): Path to the directory containing the images to process.
- `--quality`: Percentage to reduce image size (0-100).

---

## Output

- The converted images are saved in a `_converted` subdirectory inside the input directory.
- Images are named with their original base name and an index (e.g., `1_image.jpg`).
