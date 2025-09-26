import asyncio
from playwright.async_api import async_playwright
import json
from bs4 import BeautifulSoup
import sys 

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Playwright.
    """
    try:
        print(f"[INFO] Launching Chromium to fetch data for station {station_id}...")
        
        # Use async_playwright context manager for cleaner resource handling
        async with async_playwright() as p:
            # Launch Chromium browser. Playwright handles sandboxing args internally,
            # but we pass '--no-sandbox' for extra robustness in containers.
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'] 
            )
            
            page = await browser.newPage()

            await page.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

            # Use Playwright's goto. wait_until='domcontentloaded' is still supported.
            await page.goto(url, wait_until='domcontentloaded')
            
            # The API you're targeting returns JSON, so waiting 15 seconds 
            # might be unnecessary, but we keep a smaller wait for safety.
            await asyncio.sleep(5) 

            # Get the page content after JavaScript execution
            content = await page.content()

            # ... (Rest of your original parsing logic remains the same) ...
            
            # Parse the HTML content to find the JSON string within the <pre> tag
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

            # The browser will close automatically when exiting the async with block
            return available_bikes

    except Exception as e:
        print(f"[FATAL ERROR] An error occurred during data fetching: {e}", file=sys.stderr)
        return None

# ---------------------------------------------------------------------
# Main execution block (no changes needed here)
# ---------------------------------------------------------------------
async def main():
    station_id_to_find = '235'
    
    available_bikes_235 = await fetch_available_bikes(station_id_to_find)

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
