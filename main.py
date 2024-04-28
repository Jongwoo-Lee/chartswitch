import sys
import time
import atexit
import signal

from config import logger
from app import WebsocketManager, PriceManager, start_websocket_thread

def signal_handler(sig, frame):
    logger.debug("SIGINT received. Shutting down gracefully...")
    
    WebsocketManager().cleanup
    PriceManager().cleanup
    
    sys.exit(0)

def main():
    # Initiate Threads
    ws_thread = start_websocket_thread()
    
    # Register the cleanup functions to be called on exit
    atexit.register(WebsocketManager().cleanup)
    atexit.register(PriceManager().cleanup)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        print("Main thread is doing other work...")
        time.sleep(10)

if __name__ == "__main__":
    logger.debug("!! Starting new Chartswitch !!")

    # Start main
    main()