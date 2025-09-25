#!/bin/bash

# Install the Python dependencies
pip install -r requirements.txt

# Update and install Chromium
apt-get update -y
apt-get install -y chromium

# Download and install the Chromium browser for Pyppeteer
python -m pyppeteer install chromium

# Finally, start your application (replace main.py with your filename)
python main.py
