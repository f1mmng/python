import asyncio
import nest_asyncio
from pyppeteer import launch
import pyppeteer
import json
from datetime import datetime
import csv

# Apply nest_asyncio to allow running asyncio in Colab
nest_asyncio.apply()

# Ensure Chromium is downloaded
pyppeteer.install()

csv_file = "velo_data.csv"

async def fetch_available_bikes(station_id):
    """
    Fetches the number of available bikes for a specific station using Pyppeteer.
    Returns a tuple: (bikes, slots) or None if not found.
    """
    browser = None
    try:
        # Launch headless Chromium with proper flags for containers
        browser = await launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process'
            ]
        )
        page = await browser.newPage()

        # Set a realistic User-Agent
        await p
