import asyncio
from api import create_socket
from app import PriceManager
from config import logger

class WebsocketManager:
    _instance = None
    _is_initialized = False  # Flag to check if the instance has been initialized

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebsocketManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Websocket Manager: initializing the websockets.")
            self.__class__._is_initialized = True  # Set the flag indicating initialization is done

    async def start_websockets(self, symbols, intervals):
        tasks = []
        for interval in intervals:
            tasks.append(
                asyncio.create_task(
                    create_socket(symbols, interval, PriceManager())
                )
            )
        
        await asyncio.gather(*tasks)
        print("asyncio gather done")

    def cleanup(self):
        # Implement cleanup logic here, such as closing connections
        logger.debug("Websocket Manager: clean up done.")
        pass