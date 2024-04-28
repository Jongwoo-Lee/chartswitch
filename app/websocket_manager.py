import asyncio
from api import create_socket
from app import PriceManager
from config import logger

class WebsocketManager:
    _instance = None
    _is_initialized = False  # Flag to check if the instance has been initialized
    
    # Global event to signal WebSocket thread to stop
    stop_event = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebsocketManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Websocket Manager: initializing the websockets.")
            self.stop_event = asyncio.Event()

            # Set the flag indicating initialization is done
            self.__class__._is_initialized = True  

    async def start_websockets(self, symbols, intervals):
        tasks = []
        for interval in intervals:
            tasks.append(
                asyncio.create_task(
                    create_socket(symbols, interval, self.stop_event, PriceManager())
                )
            )
        
        await asyncio.gather(*tasks)

    def cleanup(self):
        # Implement cleanup logic here, such as closing connections
        self.stop_event.set()

        logger.debug("Websocket Manager: clean up done.")
        pass