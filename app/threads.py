import threading
import asyncio

from config import logger, SYMBOL_NUM, INTERVALS
from app import WebsocketManager
from api import fetch_top_symbols

def start_websocket_thread():
    ws_thread = threading.Thread(target=async_websocket_threads)
    ws_thread.start()
    return ws_thread

def async_websocket_threads():
    asyncio.run(websocket_thread())

async def websocket_thread():
    logger.debug("Websocket Thread started")

    try:
        # Start websocket loops
        await WebsocketManager().start_websockets(
            fetch_top_symbols(n=SYMBOL_NUM), INTERVALS)
    except KeyboardInterrupt:
        logger.warning("Websocket Manager Script interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
