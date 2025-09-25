import asyncio
from pyppeteer import launch
import json
from bs4 import BeautifulSoup
import shutil


def find_chromium():
    """
    Detect the correct Chromium binary in the Railway container.
    """
    possible_binaries = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]
    for name in possible_binaries:
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError("Chromium not found. Did you add it to apt.txt?")


async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    browser = None
    try:
        executable_path = find_chromium()
        possible_binaries = ["google-chrome-stable", "chromium", "chromium-browser", "google-chrome"]


        browser = await launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath=executable_path
        )
        page = await browser.newPage()

        # Optional: fake a normal browser user-agent
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        # Go to the station status page
        await page.goto(url, {'waitUntil': 'domcontentloaded'})

        # Give it a few seconds in case JS needs to render
        await asyncio.sleep(3)

        # Extract page content
        content = await page.content()

        # Parse JSON inside <pre>
        soup = BeautifulSoup(content, "html.parser")
        pre_tag = soup.find("pre")
        if not pre_tag:
            print("Could not find JSON in <pre> tag.")
            return None

        station_data = json.loads(pre_tag.get_text())

        # Find your station
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


# Run the script
if __name__ == "__main__":
    station_id_to_find = "235"
    available_bikes = asyncio.run(fetch_available_bikes(station_id_to_find))

    if available_bikes is not None:
        print(f"Available bikes for station {station_id_to_find}: {available_bikes}")
    else:
        print(f"Could not retrieve available bikes for station {station_id_to_find}.")

