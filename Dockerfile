# Use Python 3.12 slim base image
FROM python:3.12-slim

# Install necessary dependencies (e.g., git for GitHub installations)
RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Set the working directory in the container
WORKDIR /app

# Copy your project files into the container
COPY . /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port 8080 (for web servers or other network services)
EXPOSE 8080

# Define the command to run the bot when the container starts
CMD ["python", "bot.py"]
