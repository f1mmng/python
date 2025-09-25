import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_available_bikes_playwright(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a given station ID using Playwright.
    """
    async with async_playwright() as p:
        try:
            # Playwright handles the browser executable for you
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # The URL directly returns JSON, so we can get the response content
            response = await page.goto(url, wait_until="domcontentloaded")
            
            if response.status != 200:
                print(f"Failed to fetch data. Status code: {response.status}")
                return None

            station_data = await response.json()

            for station in station_data:
                if str(station.get("id")) == str(station_id):
                    return station.get("availability", {}).get("bikes")
            
            return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            if 'browser' in locals() and browser:
                await browser.close()

if __name__ == "__main__":
    station_id_to_find = "235"
    bikes = asyncio.run(fetch_available_bikes_playwright(station_id_to_find))

    if bikes is not None:
        print(f"Available bikes for station {station_id_to_find}: {bikes}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")
