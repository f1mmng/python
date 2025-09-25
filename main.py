import asyncio
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Playwright.
    """
    browser = None
    try:
        async with async_playwright() as p:
            # Launch headless Chromium
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = await browser.new_page()

            # Optional: set a realistic User-Agent
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.124 Safari/537.36"
            })

            # Navigate to the API endpoint
            await page.goto(url, wait_until="domcontentloaded")

            # Get JSON content from <pre> tag
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            pre_tag = soup.find("pre")
            if not pre_tag:
                print("Could not find <pre> tag with JSON data.")
                return None

            station_data = json.loads(pre_tag.get_text())

            # Find the available bikes for the specific station ID
            for station in station_data:
                if str(station.get("id")) == str(station_id):
                    availability = station.get("availability", {})
                    return availability.get("bikes")

            return None

    except Exception as e:
        print(f"An error occurred during data fetching: {e}")
        return None
    finally:
        if browser:
            await browser.close()


# Example usage
if __name__ == "__main__":
    station_id_to_find = "235"
    available_bikes = asyncio.run(fetch_available_bikes(station_id_to_find))

    if available_bikes is not None:
        print(f"Available bikes for station {station_id_to_find}: {available_bikes}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")
