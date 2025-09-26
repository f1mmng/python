import asyncio
from playwright.async_api import async_playwright
import json
import datetime

# --- Configuration ---
STATION_ID = "235"
API_URL = "https://www.velo-antwerpen.be/api/map/stationStatus"
CHECK_INTERVAL_MINUTES = 30
# Set a short, explicit timeout for the page load (15 seconds)
PAGE_LOAD_TIMEOUT_MS = 15000 
# ---------------------

async def fetch_available_bikes(station_id, url):
    """
    Fetches the number of available bikes for a specific station using Playwright.
    Includes robust error checking and mimicking a human browser.
    """
    browser = None
    async with async_playwright() as p:
        try:
            # 1. Launch Browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 2. Set realistic headers
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.velo-antwerpen.be/",
                "Connection": "keep-alive"
            })

            # 3. Fetch the API data with an explicit timeout
            response = await page.goto(
                url, 
                wait_until="domcontentloaded", 
                timeout=PAGE_LOAD_TIMEOUT_MS
            )
            
            status_code = response.status
            print(f"HTTP Status Code Received: {status_code}")

            if status_code != 200:
                print(f"ERROR: Server returned status code {status_code}. Cannot fetch data.")
                error_content = await response.text()
                print(f"Server Response Preview: {error_content[:500]}...")
                return None

            # 4. Parse JSON Data
            station_data = await response.json()

            # 5. Find the target station (ID is a string in the API)
            for station in station_data:
                if station.get("id") == station_id:
                    return station.get("availability", {}).get("bikes")
            
            print(f"Station with ID {station_id} not found in the data.")
            return None

        except Exception as e:
            # This catches Playwright TimeoutError or connection issues
            print(f"CRITICAL ERROR during fetching: {e}")
            return None
        finally:
            if browser:
                await browser.close()
                print("Browser closed successfully.")

async def main_loop():
    """
    The main continuous loop to fetch bike data at a defined interval.
    """
    delay_seconds = CHECK_INTERVAL_MINUTES * 60
    
    # 🌟 START MESSAGE: Confirms Python script is running 🌟
    print("--- 🚀 SCRIPT INITIATED: Python Code Execution Started Successfully 🚀 ---")
    
    print(f"Starting Velo Antwerp checker for station {STATION_ID}. Interval: {CHECK_INTERVAL_MINUTES} minutes.")
    
    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- [{timestamp}] Starting data fetch ---")
            
            bikes = await fetch_available_bikes(STATION_ID, API_URL)

            if bikes is not None:
                print(f"SUCCESS: Available bikes for station {STATION_ID}: {bikes}")
            else:
                print(f"FAILURE: Could not retrieve available bikes for station {STATION_ID}. Check logs for HTTP Status Code or Timeout error.")
            
        except Exception as e:
            # Catches unexpected errors that occur outside the fetch function
            print(f"UN
