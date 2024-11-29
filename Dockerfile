# Use the official slim Python 3.12 image
FROM python:3.12-slim

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Update the package list and install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    wget \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app/

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Expose the desired port
EXPOSE 8080

# Define the default command
CMD ["python", "bot.py"]
