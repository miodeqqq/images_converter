FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    software-properties-common \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libheif-dev \
    libraw-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libjpeg-turbo-progs \
    libavif-dev \
    expect \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY poetry.lock pyproject.toml /src/

RUN pip install --no-cache-dir poetry==1.8.5 && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . /src

ENTRYPOINT ["unbuffer", "poetry", "run", "python", "main.py"]
