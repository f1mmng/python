import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Define the station ID you want to track
# Use environment variables for configuration flexibility in Railway
STATION_ID_TO_FIND = os.environ.get('STATION_ID', '235')
LOG_PREFIX = "[VELO_DATA]" # Used to easily filter data points in Railway logs

async def fetch_available_bikes_playwright(station_id):
    """
    Fetches the number of available bikes and slots for a specific station using Playwright.
    Returns a tuple: (bikes, slots) or None if not found.
    """
    browser = None
    try:
        async with async_playwright() as p:
            # Set arguments for better compatibility in various container environments
            browser = await p.chromium.launch(
                headless=True, 
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            page = await browser.newPage()

            # Navigate to the Velo Antwerpen map page
            await page.goto("https://www.velo-antwerpen.be/nl/fiets-vinden", wait_until="domcontentloaded")

            # Wait for the necessary data to load (The station markers should confirm the map is ready)
            # You might need to adjust this selector if the site changes.
            await page.wait_for_selector('div.station-marker', timeout=15000)

            # Extract station data from the page's initial state object
            stations_json = await page.evaluate("""
                () => {
                    try {
                        // Velo Antwerpen often stores data in a window variable like __INITIAL_STATE__
                        return JSON.stringify(window.__INITIAL_STATE__.stations);
                    } catch(e) {
                        return null;
                    }
                }
            """)

            if not stations_json:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Could not extract station JSON from page.")
                return None

            stations = json.loads(stations_json)
            # Find the specific station
            station = next((s for s in stations if s['id'] == station_id), None)

            if not station:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Station {station_id} not found.")
                return None

            bikes = station['availability']['bikes']
            slots = station['availability']['slots']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log the data line to stdout (Railway logs) for persistence
            # Format: TIMESTAMP,STATION_ID,BIKES,SLOTS
            print(f"{LOG_PREFIX} {timestamp},{station_id},{bikes},{slots}")

            return bikes, slots

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FATAL ERROR during data fetching: {e}")
        return None
    finally:
        if browser:
            await browser.close()


async def main():
    """Main function to orchestrate the data fetching."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INFO: Starting data fetch for station {STATION_ID_
