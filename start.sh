#!/bin/bash

# 1. Check if the Playwright browsers are already installed in the cache location.
# This step ensures the container is ready.
echo "Checking for Playwright browsers..."

# If the folder doesn't exist, run the installation.
if [ ! -d "/root/.cache/ms-playwright/chromium-*" ]; then
    echo "Playwright browsers not found. Running installation..."
    # The 'chromium' target is essential.
    playwright install chromium
else
    echo "Playwright browsers found in cache."
fi

# 2. Start the main Python application
echo "Starting main application..."
python main.py
