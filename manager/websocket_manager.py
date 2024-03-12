import asyncio
from api import create_socket
from manager import PriceManager

class WebsocketManager:
    _instance = None
    _is_initialized = False  # Flag to check if the instance has been initialized

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebsocketManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            print("Thread manager: initializing the threads.")
            self.__class__._is_initialized = True  # Set the flag indicating initialization is done

    async def start_websockets(self, symbols, intervals):
        tasks = []
        for interval in intervals:
            tasks.append(asyncio.create_task(create_socket(symbols, interval, PriceManager())))
        await asyncio.gather(*tasks)