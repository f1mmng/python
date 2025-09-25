#!/bin/bash

# Install the Python dependencies
pip install -r requirements.txt

# Download and install the Chromium browser for Pyppeteer
python -m pyppeteer install chromium

# Finally, start your application (replace main.py with your filename)
python main.py
