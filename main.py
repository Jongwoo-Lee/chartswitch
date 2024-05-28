import signal
import threading
import time

from util import logger, configure_logging 
from app import WebsocketManager, start_websocket_thread

websocket_event = threading.Event()
price_thread_event = threading.Event()

def signal_handler(sig, frame):
    logger.info(f"Signal {sig} received. Shutting down gracefully...")

    WebsocketManager().cleanup()


def main(production_mode = False):
    logger.info(production_mode)
    configure_logging(production_mode)

    logger.info("############## Starting new Chartswitch ##############")

    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initiate Threads
    start_websocket_thread(websocket_event)

    # Do Some Price Calculation
    while not websocket_event.is_set():
        time.sleep(4)

    websocket_event.wait()

    logger.debug("Websocket threads are closed successfully")
    logger.info("Exiting main...")

if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run the application.')
    parser.add_argument('--prod', action='store_true', help='Run in production mode without debug logging')
    args = parser.parse_args()

    # Start main
    main(production_mode=args.prod)