import asyncio
from playwright.async_api import async_playwright
import json
from bs4 import BeautifulSoup
import sys 

# Define the station ID you are interested in
station_id_to_find = '235'

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Playwright.
    """
    try:
        print(f"[INFO] Launching Chromium to fetch data for station {station_id}...")
        
        # Use async_playwright context manager for cleaner resource handling
        async with async_playwright() as p:
            # Launch Chromium browser with necessary args for container environment
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'] 
            )
            
            # FIX: Correct Playwright syntax is browser.new_page()
            page = await browser.new_page() 

            await page.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

            await page.goto(url, wait_until='domcontentloaded')
            
            # Keep a reasonable wait time for full content loading
            await asyncio.sleep(5) 

            # Get the page content after JavaScript execution
            content = await page.content()

            # Parse the content to find and load the JSON
            soup = BeautifulSoup(content, 'html.parser')
            pre_tag = soup.find('pre')
            station_data = None
            
            if pre_tag:
                json_string = pre_tag.get_text()
                try:
                    station_data = json.loads(json_string)
                    print("[INFO] Successfully parsed JSON data.")
                except json.JSONDecodeError:
                    print("[ERROR] Error decoding extracted JSON string.")
                    return None
            else:
                print("[ERROR] Could not find <pre> tag with JSON data in page content.")
                return None

            # Find the available bikes for the specific station ID
            available_bikes = None
            if station_data:
                for station in station_data:
                    if station.get('id') == station_id:
                        availability = station.get('availability')
                        if availability and isinstance(availability, dict):
                            available_bikes = availability.get('bikes')
                        break

            # Browser is automatically closed by the 'async with' block
            return available_bikes

    except Exception as e:
        # Catch and report fatal errors during the fetching process
        print(f"[FATAL ERROR] An error occurred during data fetching: {e}", file=sys.stderr)
        return None

# ---------------------------------------------------------------------
# Main execution block
# ---------------------------------------------------------------------
async def main():
    """
    Defines the entry point and execution logic for the script.
    """
    available_bikes_235 = await fetch_available_bikes(station_id_to_find)

    # Print the final result
    if available_bikes_235 is not None:
        print(f"✅ Available bikes for station {station_id_to_find}: {available_bikes_235}")
    else:
        print(f"❌ Could not retrieve available bikes for station {station_id_to_find}.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"A fatal error occurred in the main execution block: {e}", file=sys.stderr)
        sys.exit(1)
