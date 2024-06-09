import asyncio
from typing import List
from api import create_socket
from app import PriceManager
from util import logger, INTERVALS

class WebsocketManager:
    _instance = None
    _is_initialized = False  # Flag to check if the instance has been initialized
    stop_event: asyncio.Event = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WebsocketManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Initializing Websocket Manager")
            
            # Signal WebSocket to stop
            self.stop_event = asyncio.Event()

            # Set the flag indicating initialization is done
            self.__class__._is_initialized = True  

    async def start_websockets(self):
        tasks: List[asyncio.Task] = []
        for interval in INTERVALS:
            logger.debug(f"Creating websockets coroutines for {interval} intervak price updates")

            tasks.append(
                asyncio.create_task(
                    create_socket(self.stop_event)
                )
            )
        
        await asyncio.gather(*tasks)
        
        # Cancel all WebSocket tasks
        for task in tasks:
            task.cancel()
        
        logger.debug("Cancelled all websockets")

    def cleanup(self):
        # Implement cleanup logic here, such as closing connections
        self.stop_event.set()