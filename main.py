import asyncio
import atexit
import signal
import sys

from manager import WebsocketManager, PriceManager
from api import fetch_top_symbols
from config import INTERVALS, UPDATE_INTERVAL, SYMBOL_NUM, logger

async def main():
    
    # Create a global instance of the class
    ws_manager = WebsocketManager()
    price_manager = PriceManager()

    try:
        while True:
            top_symbols = fetch_top_symbols(n=SYMBOL_NUM)  # Assuming fetch_top_symbols takes 'n' as an argument
            if top_symbols:
                logger.info(f"Top {SYMBOL_NUM} symbols by daily volume: {top_symbols}")

                # Use WebsocketManager to start websockets
                await ws_manager.start_websockets(top_symbols, INTERVALS)

                # Wait for the update interval
                await asyncio.sleep(UPDATE_INTERVAL)

                # Use WebsocketManager to stop websockets
                price_manager.partial_cleanup()

            else:
                logger.error("Failed to fetch top symbols")
                break

    except KeyboardInterrupt:
        logger.warning("Websocket Manager Script interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def signal_handler(sig, frame):
    logger.debug("SIGINT received. Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    logger.debug("!! Starting new Chartswitch !!")
    ws_manager = WebsocketManager()
    price_manager = PriceManager()
    
    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    atexit.register(price_manager.cleanup)
    atexit.register(ws_manager.cleanup)

    asyncio.run(main())