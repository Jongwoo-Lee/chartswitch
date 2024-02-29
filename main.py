import asyncio
import atexit
import signal
import sys
from binance_api import fetch_top_symbols
from manager.websocket_manager import WebsocketManager
from manager.price_manager import PriceManager
from config import INTERVALS, UPDATE_INTERVAL, SYMBOL_NUM

async def start_main():
    
    # Create a global instance of the class
    ws_manager = WebsocketManager()
    price_manager = PriceManager()

    try:
        while True:
            top_symbols = fetch_top_symbols(n=SYMBOL_NUM)  # Assuming fetch_top_symbols takes 'n' as an argument
            if top_symbols:
                print(f"Top {SYMBOL_NUM} symbols by daily volume: {top_symbols}")

                # Use ThreadManager to start threads
                await ws_manager.start_websockets(top_symbols, INTERVALS)

                # Wait for the update interval
                await asyncio.sleep(UPDATE_INTERVAL)

                # Use ThreadManager to stop threads
                price_manager.partial_cleanup()

            else:
                print("Failed to fetch top symbols")
                break

    except KeyboardInterrupt:
        print("Script interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Register the cleanup function of ThreadManager to be called on exit
    ws_manager = WebsocketManager()
    price_manager = PriceManager()
    
    atexit.register(price_manager.cleanup)

    asyncio.run(start_main())