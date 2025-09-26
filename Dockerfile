# Use a suitable base image (e.g., one with necessary libs for headless browsers)
# python:3.11-slim-buster is a good, common choice
FROM python:3.11-slim-buster 

# 1. Install system dependencies for Playwright/Browsers
#    (These are minimal for Debian-based images)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libwoff1 \
        libharfbuzz-icu7 \
        libgdk-pixbuf2.0-0 \
        libcairo2 \
        libpango-1.0-0 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libgbm1 \
        libasound2 \
        libpangocairo-1.0-0 \
        libnspr4 \
        libnss3 \
        libdbus-1-3 \
        libexpat1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Use the playwright CLI to download the browser binaries
#    This is critical for Playwright to work in a clean container
RUN playwright install chromium

# 5. Copy your code
COPY . .

# 6. Set the command (ensure your script's entry point is fixed, see below)
CMD ["/bin/bash", "start.sh"] 
# OR: CMD ["python", "your_script_name.py"]
