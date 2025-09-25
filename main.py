import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Playwright.

    Args:
        station_id: The ID of the station to fetch data for.
        url: The URL of the station status API.

    Returns:
        The number of available bikes for the station, or None if the station is not found or data is unavailable.
    """
    async with async_playwright() as p:
        try:
            # Launch a headless Chromium browser using Playwright's built-in manager
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # The URL returns raw JSON, so we can fetch it directly
            response = await page.goto(url, wait_until="domcontentloaded")
            
            if response.status != 200:
                print(f"Failed to fetch data. Status code: {response.status}")
                return None

            # Parse the response body as a JSON object directly
            station_data = await response.json()

            # Find the available bikes for the specific station ID
            for station in station_data:
                # Compare the station ID as an integer for a correct match
                if station.get("id") == int(station_id):
                    return station.get("availability", {}).get("bikes")
            
            print(f"Station with ID {station_id} not found in the data.")
            return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            if 'browser' in locals() and browser:
                await browser.close()

if __name__ == "__main__":
    station_id_to_find = "235"
    bikes = asyncio.run(fetch_available_bikes(station_id_to_find))

    if bikes is not None:
        print(f"Available bikes for station {station_id_to_find}: {bikes}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")
