import asyncio
from pyppeteer import launch
import json
from bs4 import BeautifulSoup

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    browser = None
    try:
        # Launch headless Chromium installed in Railway container
        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath='/usr/bin/chromium-browser'  # Railway Chromium path
        )
        page = await browser.newPage()

        # Optional: set a realistic user agent
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        # Navigate to the API page
        await page.goto(url, {'waitUntil': 'domcontentloaded'})

        # Wait for the page to fully render JSON (if needed)
        await asyncio.sleep(5)

        # Get page content
        content = await page.content()

        # Parse the HTML and extract JSON from <pre> tag
        soup = BeautifulSoup(content, 'html.parser')
        pre_tag = soup.find('pre')
        if not pre_tag:
            print("Could not find <pre> tag with JSON data.")
            return None

        station_data = json.loads(pre_tag.get_text())

        # Find available bikes for the given station ID
        for station in station_data:
            if str(station.get('id')) == str(station_id):
                return station.get('availability', {}).get('bikes')

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if browser:
            await browser.close()


# Example usage
station_id_to_find = '235'
available_bikes = asyncio.run(fetch_available_bikes(station_id_to_find))

if available_bikes is not None:
    print(f"Available bikes for station {station_id_to_find}: {available_bikes}")
else:
    print(f"Could not retrieve available bikes for station {station_id_to_find}.")
