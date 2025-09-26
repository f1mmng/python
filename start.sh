#!/bin/bash

# 1. Install all necessary browser binaries
echo "--- Starting Playwright Browser Installation ---"
playwright install

# 2. Run the main Python application
echo "--- Starting Python Main Script ---"
# Use exec to ensure the container uses the python process as its primary process
exec python main.py
