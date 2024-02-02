import threading
from typing import List
from websocket_client import create_socket
from config import BINANCE_WS_THREAD_NAME


class ThreadManager:
    def __init__(self):
        self.threads: List[threading.Thread] = []
        self.stop_events: List[threading.Event] = []


    def start_websocket_threads(self, symbols, intervals):
        for interval in intervals:
            stop_event = threading.Event()
            self.stop_events.append(stop_event)
            thread_name = f"{BINANCE_WS_THREAD_NAME}{interval}"
            thread = threading.Thread(target=create_socket, args=(symbols, interval, stop_event), name=thread_name)
            thread.custom_attribute = "just_doublechecking_binance_websocket"  # Custom attribute
            self.threads.append(thread)
            thread.start()

    def stop_websocket_threads(self):
        for stop_event in self.stop_events:
            stop_event.set()
        for thread in self.threads:
            thread.join(timeout=5)

    def cleanup(self):
        print("Cleaning up and stopping threads...")
        self.stop_websocket_threads()

        for thread in self.threads:  # Use self to refer to the instance variable
            if thread.is_alive():
                print(f"Warning: Thread {thread.name} did not terminate")
                
        print("Clean up done")
        