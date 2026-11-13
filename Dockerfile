FROM python:3.11-slim-bookworm

# System dependencies used by media/image plugins
RUN apt-get update && apt-get install -y --no-install-recommends \
        git wget unzip zip ffmpeg mediainfo p7zip-full \
        libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the launcher/source of this repository
COPY . .

# The Eivabot package itself is fetched at runtime by the launcher script
# (see Eivabot). When running this image directly, clone the upstream core:
#   docker build --build-arg ... or provide the package via volume.
ENV PYTHONUNBUFFERED=1

CMD ["bash", "Eivabot"]
