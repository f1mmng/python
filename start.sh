#!/bin/bash

echo "🚀 Starting setup..."

# Ensure pip is up-to-date
python3 -m pip install --upgrade pip

# Install the Playwright library for Python
echo "📦 Installing Playwright library..."
pip install playwright

# Download and install the necessary browsers (Chromium, Firefox, WebKit)
echo "🌐 Installing browsers for Playwright..."
playwright install

echo "✅ Setup complete! You can now run the Python script."
