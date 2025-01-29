from pathlib import Path
from typing import List, Tuple

import pytest
from PIL import Image

from main import convert_images


@pytest.fixture
def create_images_fixture(tmp_path: "Path"):
    """
    A fixture to create a test directory with different types of images.
    """

    def _create_images(
        image_specs: List[Tuple[str, Tuple[int, int], str]]
    ) -> "Path":
        """
        Create images based on the provided specifications.
        """

        test_dir = tmp_path / "test_images"
        test_dir.mkdir()

        for file_name, dimensions, color in image_specs:
            img = Image.new(mode="RGB", size=dimensions, color=color)
            img.save(fp=test_dir / file_name)

        return test_dir

    return _create_images


def test_images_converter_creates_converted_dir(create_images_fixture) -> None:
    """
    Test that the script creates a `_converted` dir in the input directory.
    """

    tmp_dir = create_images_fixture(
        [
            ("image1.png", (100, 100), "red"),
            ("image2.jpg", (200, 200), "green"),
            ("image3.tiff", (300, 300), "blue"),
        ]
    )

    convert_images(input_dir=tmp_dir.as_posix(), quality_decrease=50)

    output_dir = tmp_dir / "_converted"

    assert output_dir.exists() and output_dir.is_dir()


def test_images_converter_converts_files(create_images_fixture) -> None:
    """
    Test that the script converts files to JPEG
    and saves them in the `_converted` dir.
    """

    tmp_dir = create_images_fixture(
        [
            ("image1.png", (100, 100), "red"),
            ("image2.jpg", (200, 200), "green"),
            ("image3.tiff", (300, 300), "blue"),
        ]
    )

    convert_images(input_dir=tmp_dir.as_posix(), quality_decrease=50)
    output_dir = tmp_dir / "_converted"

    converted_files = list(output_dir.glob("*.jpg"))

    assert len(converted_files) == 3

    for converted_image in converted_files:
        with Image.open(fp=converted_image) as img:
            assert img.format == "JPEG"


def test_images_converter_handles_empty_directory(tmp_path: Path) -> None:
    """
    Test that the script handles an empty input directory gracefully.
    """

    empty_dir = tmp_path / "empty_images"
    empty_dir.mkdir()

    convert_images(input_dir=empty_dir.as_posix(), quality_decrease=50)

    assert not (empty_dir / "_converted").exists()


def test_images_converter_handles_invalid_directory() -> None:
    """
    Test that the script raises a ValueError for a non-existent directory.
    """

    with pytest.raises(ValueError):
        convert_images(input_dir="non_existent_directory", quality_decrease=50)


def test_images_converter_handles_varied_file_types(
    create_images_fixture,
) -> None:
    """
    Test that the script processes a mix of valid and invalid image formats.
    """

    test_dir = create_images_fixture(
        [
            ("valid1.png", (100, 100), "red"),
            ("valid2.jpg", (200, 200), "green"),
        ]
    )

    invalid_file = test_dir / "invalid.txt"
    invalid_file.write_text("This is not an image.")

    convert_images(input_dir=str(test_dir), quality_decrease=50)
    output_dir = test_dir / "_converted"

    converted_files = list(output_dir.rglob("*.jpg"))

    assert len(converted_files) == 2

    for converted_image in converted_files:
        with Image.open(fp=converted_image) as img:
            assert img.format == "JPEG"


@pytest.mark.parametrize(
    "image_specs, quality_decrease, expected_sizes",
    [
        pytest.param(
            [
                ("image1.png", (400, 400), "red"),
                ("image2.jpg", (800, 800), "green"),
            ],
            50,  # 50% quality decrease
            [
                (200, 200),  # expected size for image1
                (400, 400),  # expected size for image2
            ],
            id="reduce_quality_by_50",
        ),
        pytest.param(
            [
                ("image1.png", (300, 300), "blue"),
                ("image2.jpg", (600, 600), "yellow"),
            ],
            25,  # 25% quality decrease
            [
                (225, 225),  # expected size for image1
                (450, 450),  # expected size for image2
            ],
            id="reduce_quality_by_25",
        ),
        pytest.param(
            [
                ("image1.png", (500, 500), "purple"),
                ("image2.jpg", (1000, 1000), "orange"),
            ],
            0,  # no quality decrease
            [
                (500, 500),  # expected size for image1
                (1000, 1000),  # expected size for image2
            ],
            id="no_quality_decrease",
        ),
    ],
)
def test_images_converter_respects_quality(
    create_images_fixture, image_specs, quality_decrease, expected_sizes
):
    """
    Test that the script correctly reduces image dimensions based on quality.
    """

    test_dir = create_images_fixture(image_specs)

    convert_images(
        input_dir=test_dir.as_posix(), quality_decrease=quality_decrease
    )
    output_dir = test_dir / "_converted"

    converted_files = list(output_dir.rglob("*.jpg"))

    assert len(converted_files) == len(image_specs)

    for converted_image, expected_size in zip(converted_files, expected_sizes):
        with Image.open(fp=converted_image) as img:
            assert img.format == "JPEG"
            assert img.size == expected_size
