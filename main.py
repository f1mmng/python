async def main_loop():
    """
    The main continuous loop to fetch bike data at a defined interval.
    """
    delay_seconds = CHECK_INTERVAL_MINUTES * 60
    
    # 🌟 START MESSAGE: Confirms Python script is running 🌟
    print("--- 🚀 SCRIPT INITIATED: Python Code Execution Started Successfully 🚀 ---")
    
    print(f"Starting Velo Antwerp checker for station {STATION_ID}. Interval: {CHECK_INTERVAL_MINUTES} minutes.")
    
    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- [{timestamp}] Starting data fetch ---")
            
            bikes = await fetch_available_bikes(STATION_ID, API_URL)

            if bikes is not None:
                print(f"SUCCESS: Available bikes for station {STATION_ID}: {bikes}")
            else:
                print(f"FAILURE: Could not retrieve available bikes for station {STATION_ID}. Check logs for HTTP Status Code or Timeout error.")
            
        except Exception as e:
            # THIS IS THE CORRECTED BLOCK (assuming this was around line 96)
            print(f"UNHANDLED ERROR in main loop: {e}") 
            
        finally:
            print(f"Sleeping for {CHECK_INTERVAL_MINUTES} minutes...")
            await asyncio.sleep(delay_seconds)
