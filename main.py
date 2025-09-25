import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Playwright.
    """
    async with async_playwright() as p:
        try:
            # Launch a headless Chromium browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Set a more comprehensive and realistic set of headers
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.velo-antwerpen.be/",
                "Connection": "keep-alive"
            })

            # The URL returns raw JSON
            response = await page.goto(url, wait_until="domcontentloaded")

            if response.status != 200:
                print(f"Failed to fetch data. Status code: {response.status}")
                return None

            station_data = await response.json()

            for station in station_data:
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
