# Use the stable 'bullseye' (Debian 11) base image. 
FROM python:3.11-slim-bullseye 

# 1. Install necessary system packages for Playwright/Chromium.
# This list now includes the missing dependencies from the Playwright warning (libxkbcommon0, etc.).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        # Core rendering dependencies
        libwoff1 \
        libharfbuzz-icu0 \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        # General UI/Browser dependencies
        libgdk-pixbuf2.0-0 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libgbm1 \
        libasound2 \
        libnspr4 \
        libnss3 \
        libdbus-1-3 \
        libexpat1 \
        # === NEW DEPENDENCIES FROM WARNING ===
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        # =====================================
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Copy and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. CRITICAL: Download the browser binaries (Chromium) inside the container
RUN playwright install chromium

# 5. Copy your application code and startup script
COPY main.py .
COPY start.sh .

# 6. Set execute permissions for the startup script
RUN chmod +x start.sh

# 7. Use the startup script as the default command for the cron job
CMD ["/bin/bash", "start.sh"]
