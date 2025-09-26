import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
import csv

csv_file = "velo_data.csv"

async def fetch_available_bikes_playwright(station_id):
    """
    Fetches the number of available bikes and slots for a specific station using Playwright.
    Returns a tuple: (bikes, slots) or None if not found.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.newPage()

        try:
            # Navigate to the Velo Antwerpen map page
            await page.goto("https://www.velo-antwerpen.be/nl/fiets-vinden", wait_until="domcontentloaded")

            # Wait for the necessary data to load. This might require inspecting the page's network requests or DOM.
            # As a starting point, we'll wait for a selector that appears after the data is likely loaded.
            # You might need to adjust this selector based on the actual page structure.
            await page.wait_for_selector('div.station-marker', timeout=10000) # Example selector

            # Extract station data from the page. This might involve evaluating JavaScript
            # or scraping the DOM based on how the data is presented.
            # Based on the previous attempt, let's try to access window.__INITIAL_STATE__.stations again.
            stations_json = await page.evaluate("""
                () => {
                    try {
                        return JSON.stringify(window.__INITIAL_STATE__.stations);
                    } catch(e) {
                        return null;
                    }
                }
            """)

            if not stations_json:
                print("Could not extract station JSON from page.")
                return None

            stations = json.loads(stations_json)
            station = next((s for s in stations if s['id'] == station_id), None)

            if not station:
                print(f"Station {station_id} not found.")
                return None

            bikes = station['availability']['bikes']
            slots = station['availability']['slots']

            # Save to CSV with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, bikes, slots])

            return bikes, slots

        except Exception as e:
            print(f"An error occurred during data fetching: {e}")
            return None
        finally:
            await browser.close()


# Define the station ID you want to track
station_id_to_find = '235'

# Fetch data and print result
available_bikes_slots = await fetch_available_bikes_playwright(station_id_to_find)

if available_bikes_slots:
    print(f"Station {station_id_to_find} - Bikes: {available_bikes_slots[0]}, Slots: {available_bikes_slots[1]}")
else:
    print(f"Could not retrieve available bikes for station {station_id_to_find}.")
