import threading
from typing import List
from websocket_client import create_socket
from config import BINANCE_WS_THREAD_NAME


class ThreadManager:
    _instance = None
    _lock = threading.Lock()  # Class-level lock
    _is_initialized = False  # Flag to check if the instance has been initialized

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            print("Thread manager: initializing the threads.")
            self.threads: List[threading.Thread] = []
            self.stop_events: List[threading.Event] = []
            self.__class__._is_initialized = True  # Set the flag indicating initialization is done

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
        print("Thread manager: Cleaning up and stopping threads...")
        self.stop_websocket_threads()

        for thread in self.threads:  # Use self to refer to the instance variable
            if thread.is_alive():
                print(f"Warning: Thread {thread.name} did not terminate")
                
        print("Thread manager: Clean up done")
        