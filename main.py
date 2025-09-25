import asyncio
from pyppeteer import launch
import json
from datetime import datetime
import csv

station_id = "001"  # your station ID
csv_file = "velo_data.csv"

async def fetch_station_data():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://www.velo-antwerpen.be/nl/fiets-vinden')
    await asyncio.sleep(5)
    content = await page.evaluate('() => document.body.innerText')
    await browser.close()
    return content

data_text = asyncio.get_event_loop().run_until_complete(fetch_station_data())

try:
    stations = json.loads(data_text)
    station = next(s for s in stations if s['id'] == station_id)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bikes = station['availability']['bikes']
    slots = station['availability']['slots']
    
    # Save to CSV
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, bikes, slots])
    
    print(f"{timestamp} - Bikes: {bikes}, Slots: {slots}")

except Exception as e:
    print("Error:", e)
