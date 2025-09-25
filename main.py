import asyncio
from pyppeteer import launch
import json
from datetime import datetime
import csv

station_id = '235'
csv_file = "velo_data.csv"

async def fetch_available_bikes(station_id):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    
    # Use a realistic User-Agent
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    try:
        await page.goto("https://www.velo-antwerpen.be/nl/fiets-vinden", {'waitUntil': 'domcontentloaded'})
        await asyncio.sleep(5)  # wait for JavaScript to load
        
        # Evaluate JS in the page to extract the station JSON from the global variable
        # Velo site often stores stations in window.__INITIAL_STATE__ or similar
        stations_json = await page.evaluate("""
            () => {
                try {
                    return JSON.stringify(window.__INITIAL_STATE__.stations);
                } catch(e) {
                    return null;
                }
            }
        """)
        
        if not stations_json:
            print("Could not extract station JSON from page.")
            return None
        
        stations = json.loads(stations_json)
        station = next((s for s in stations if s['id'] == station_id), None)
        
        if not station:
            print(f"Station {station_id} not found.")
            return None
        
        bikes = station['availability']['bikes']
        slots = station['availability']['slots']
        
        # Log to CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, bikes, slots])
        
        return bikes, slots
    
    finally:
        await browser.close()

# Run the async function
bikes_slots = asyncio.get_event_loop().run_until_complete(fetch_available_bikes(station_id))
if bikes_slots:
    print(f"Station {station_id} - Bikes: {bikes_slots[0]}, Slots: {bikes_slots[1]}")
