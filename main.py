import asyncio
import nest_asyncio
from pyppeteer import launch
import json
from bs4 import BeautifulSoup

# Apply nest_asyncio to allow running asyncio in Colab
nest_asyncio.apply()

async def fetch_available_bikes(station_id, url="https://www.velo-antwerpen.be/api/map/stationStatus"):
    """
    Fetches the number of available bikes for a specific station using Pyppeteer.

    Args:
        station_id: The ID of the station to fetch data for.
        url: The URL of the station status API.

    Returns:
        The number of available bikes for the station, or None if the station is not found or data is unavailable.
    """
    browser = None  # Initialize browser to None
    try:
        # Launch a headless Chromium browser
        browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()

        # Set a realistic User-Agent (optional, can help with some sites)
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # print(f"Navigating to {url}...")
        # Use 'domcontentloaded' or 'load' as 'networkidle0' can sometimes wait indefinitely
        await page.goto(url, {'waitUntil': 'domcontentloaded'})

        # Wait for potential WAF challenges or JavaScript loading
        # This time might need adjustment based on observation
        await asyncio.sleep(15)

        # Get the page content after JavaScript execution
        content = await page.content()

        # Parse the HTML content to find the JSON string within the <pre> tag
        soup = BeautifulSoup(content, 'html.parser')
        pre_tag = soup.find('pre')

        station_data = None
        if pre_tag:
            json_string = pre_tag.get_text()
            try:
                station_data = json.loads(json_string)
                # print("Successfully parsed JSON data.")
            except json.JSONDecodeError:
                print("Error decoding extracted JSON string.")
                return None
        else:
            print("Could not find <pre> tag with JSON data in page content.")
            return None

        # Find the available bikes for the specific station ID
        available_bikes = None
        if station_data:
            for station in station_data:
                if station.get('id') == station_id:
                    # Access availability and bikes using .get() for safety
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

# Define the station ID you are interested in
station_id_to_find = '235'

# Call the async function to fetch data and print the result
available_bikes_235 = await fetch_available_bikes(station_id_to_find)

if available_bikes_235 is not None:
    print(f"Available bikes for station {station_id_to_find}: {available_bikes_235}")
else:
    print(f"Could not retrieve available bikes for station {station_id_to_find}.")
