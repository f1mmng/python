import asyncio
from pyppeteer import launch
import json

station_id = "001"

async def fetch_station_data():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://www.velo-antwerpen.be/nl/fiets-vinden')
    await asyncio.sleep(5)  # wait for page to load
    content = await page.evaluate('() => document.body.innerText')
    await browser.close()
    return content

data_text = asyncio.get_event_loop().run_until_complete(fetch_station_data())

try:
    stations = json.loads(data_text)
    station = next(s for s in stations if s['id'] == station_id)
    print(f"Station ID: {station['id']}")
    print(f"Available bikes: {station['availability']['bikes']}")
except Exception as e:
    print("Error:", e)