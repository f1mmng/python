import asyncio
# import nest_asyncio # REMOVED: This is for Google Colab only.
from pyppeteer import launch
import json
from bs4 import BeautifulSoup
import sys 
import os # Added for potential future use or debugging

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Pyppeteer.

    Args:
        station_id: The ID of the station to fetch data for.
        url: The URL of the station status API.

    Returns:
        The number of available bikes for the station, or None if the station is not found or data is unavailable.
    """
    browser = None
    try:
        print(f"[INFO] Launching Chromium to fetch data for station {station_id}...")
        
        # ---------------------------------------------------------------------
        # CRITICAL: Arguments for running in a container/headless environment
        # --no-sandbox and --disable-setuid-sandbox prevent privilege issues.
        # --disable-dev-shm-usage prevents out-of-memory errors in low-resource environments.
        # ---------------------------------------------------------------------
        browser = await launch(
            headless=True,
            args=[
                '--no-sandbox', 
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        page = await browser.newPage()

        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        await page.goto(url, {'waitUntil': 'domcontentloaded'})
        
        # Wait period adjusted for potential network or WAF delay
        await asyncio.sleep(15) 

        # Get the page content after JavaScript execution
        content = await page.content()

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
                print("Error decoding extracted JSON string.")
                return None
        else:
            print("Could not find <pre> tag with JSON data in page content.")
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

        return available_bikes

    except Exception as e:
        # Use sys.stderr for error messages in a standard logging practice
        print(f"[ERROR] An error occurred during data fetching: {e}", file=sys.stderr)
        return None
    finally:
        if browser:
            print("[INFO] Closing browser.")
            await browser.close()

# ---------------------------------------------------------------------
# Main function to run the asynchronous code
# ---------------------------------------------------------------------
async def main():
    """
    Defines the entry point and execution logic for the script.
    """
    station_id_to_find = '235'
    
    # Execute the asynchronous fetch function
    available_bikes_235 = await fetch_available_bikes(station_id_to_find)

    # Print the final result
    if available_bikes_235 is not None:
        print(f"✅ Available bikes for station {station_id_to_find}: {available_bikes_235}")
    else:
        print(f"❌ Could not retrieve available bikes for station {station_id_to_find}.")
        # Exit with a non-zero code to indicate failure if needed
        # sys.exit(1) 

# ---------------------------------------------------------------------
# Standard execution block
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Standard Python way to run the main async function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        print(f"A fatal error occurred in the main execution block: {e}", file=sys.stderr)
        sys.exit(1)
