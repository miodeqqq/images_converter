.PHONY: clean build_image pylint black tests

clean:
	clear;rm -rf ./.cache/ && \
    rm -rf .DS_Store && \
    rm -rf .idea && \
    rm -rf assets && \
    find . -name ".DS_Store" -print -delete && \
    find . -name "*.pyc" -exec rm -f {} \; && \
    find . -name "*.html" -exec rm -f {} \; && \
    find . -type d -name __pycache__ -exec rm -r {} \+

build_image:
	clear;docker build -t images_converter .

pylint:
	clear;poetry run pylint .

black:
	clear;poetry run black .

tests:
	clear;poetry run pytest -v
