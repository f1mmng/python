#!/bin/bash

echo "Running Playwright install to check/download browsers..."
playwright install chromium

echo "Starting main application..."
python main.py
