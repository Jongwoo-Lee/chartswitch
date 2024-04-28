import sys
import time
import atexit
import signal

from config import logger
from app import WebsocketManager, PriceManager, start_websocket_thread

def signal_handler(sig, frame):
    logger.debug("SIGINT received. Shutting down gracefully...")
    sys.exit(0)

def main():
    start_websocket_thread()
    while True:
        print("Main thread is doing other work...")
        # Perform other tasks synchronously or asynchronously
        time.sleep(10)  # Example of asynchronous task in the main thread

if __name__ == "__main__":
    logger.debug("!! Starting new Chartswitch !!")

    # Initiate Global Singleton Classes
    ws_manager = WebsocketManager()
    price_manager = PriceManager()
    
    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    atexit.register(price_manager.cleanup)
    atexit.register(ws_manager.cleanup)

    # Start main
    main()