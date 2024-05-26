import signal
import threading
import time

from config import logger
from app import WebsocketManager, start_websocket_thread

websocket_event = threading.Event()
price_thread_event = threading.Event()

def signal_handler(sig, frame):
    logger.debug(f"Signal {sig} received. Shutting down gracefully...")
    print(f"Signal {sig} received. Shutting down gracefully...")

    WebsocketManager().cleanup()


def main():
    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initiate Threads
    start_websocket_thread(websocket_event)

    # Do Some Price Calculation
    while not websocket_event.is_set():
        print("do nothing")
        time.sleep(4)
    websocket_event.wait()
    logger.debug("Websocket threads are closed successfully")
    
    logger.debug("Exiting main...")
    print("Exiting main...")


if __name__ == "__main__":
    logger.debug("############## Starting new Chartswitch ##############")

    # Start main
    main()