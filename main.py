import asyncio
from pyppeteer import launch
import json
from bs4 import BeautifulSoup

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a given station ID.
    """
    browser = None
    try:
        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath='/usr/bin/chromium'  # Direct path to the Chromium executable
        )
        page = await browser.newPage()

        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )

        await page.goto(url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(3)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        pre_tag = soup.find("pre")
        if not pre_tag:
            print("Could not find JSON in <pre> tag.")
            return None

        station_data = json.loads(pre_tag.get_text())

        for station in station_data:
            if str(station.get("id")) == str(station_id):
                return station.get("availability", {}).get("bikes")

        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if browser:
            await browser.close()


if __name__ == "__main__":
    station_id_to_find = "235"
    bikes = asyncio.run(fetch_available_bikes(station_id_to_find))

    if bikes is not None:
        print(f"Available bikes for station {station_id_to_find}: {bikes}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")
