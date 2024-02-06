import time
import atexit
import signal
import sys
from binance_api import fetch_top_symbols
from thread_manager import ThreadManager
from config import INTERVALS, UPDATE_INTERVAL, SYMBOL_NUM

def start_main(thread_manager: ThreadManager):
    try:
        while True:
            top_10_symbols = fetch_top_symbols(n=SYMBOL_NUM)  # Assuming fetch_top_symbols takes 'n' as an argument
            if top_10_symbols:
                print("Top 10 symbols by daily volume:", top_10_symbols)

                # Use ThreadManager to start threads
                thread_manager.start_websocket_threads(top_10_symbols, INTERVALS)

                # Wait for the update interval
                time.sleep(UPDATE_INTERVAL)

                # Use ThreadManager to stop threads
                thread_manager.stop_websocket_threads()

            else:
                print("Failed to fetch top symbols")
                break

    except KeyboardInterrupt:
        print("Script interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")

def signal_handler(sig, frame):
    print('Received shutdown signal. Shutting down gracefully.')
    thread_manager.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    # Register the cleanup function of ThreadManager to be called on exit
    thread_manager = ThreadManager()
    
    atexit.register(thread_manager.cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    start_main(thread_manager)