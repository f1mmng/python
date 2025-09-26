import asyncio
# import nest_asyncio # REMOVE this, it's for Colab only
from pyppeteer import launch
import json
from bs4 import BeautifulSoup

# Define the async function as is (no changes needed inside)
async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    # ... (Your function body remains the same)
    """
    Fetches the number of available bikes for a specific station using Pyppeteer.
    ...
    """
    browser = None
    try:
        # Crucial for Railway/headless environments: use 'executablePath'
        # The 'args' are also critical for running in a non-root environment
        # Pyppeteer attempts to find Chromium, but specifying the path is safer.
        # However, for Railway, pyppeteer's auto-download may work if dependencies are met.
        # We will focus on the args first:
        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.newPage()
        # ... (Rest of your original code remains the same)
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        await page.goto(url, {'waitUntil': 'domcontentloaded'})
        await asyncio.sleep(15)
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        pre_tag = soup.find('pre')
        station_data = None
        if pre_tag:
            json_string = pre_tag.get_text()
            try:
                station_data = json.loads(json_string)
            except json.JSONDecodeError:
                print("Error decoding extracted JSON string.")
                return None
        else:
            print("Could not find <pre> tag with JSON data in page content.")
            return None

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
        print(f"An error occurred during data fetching: {e}")
        return None
    finally:
        if browser:
            await browser.close()

# Define the main execution block
async def main():
    station_id_to_find = '235'
    available_bikes_235 = await fetch_available_bikes(station_id_to_find)

    if available_bikes_235 is not None:
        print(f"Available bikes for station {station_id_to_find}: {available_bikes_235}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")

# Standard way to run the async main function
if __name__ == "__main__":
    asyncio.run(main())
