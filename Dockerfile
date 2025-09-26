# Use the official, pre-built Playwright Docker image as the base.
# This image includes Node.js, Python, and all necessary browser dependencies (Chromium, Firefox, WebKit).
FROM mcr.microsoft.com/playwright/python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Python dependencies file
COPY requirements.txt .

# Install the Python dependencies (Playwright is already installed, but we need beautifulsoup4)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Ensure the start script is executable (if you are still using start.sh)
RUN chmod +x start.sh

# Define the command to run the application (using your start.sh script)
# The CMD is executed when the container starts.
CMD ["/bin/bash", "start.sh"]
