import threading
import asyncio

from config import logger, SYMBOL_NUM, INTERVALS
from app import WebsocketManager
from api import fetch_top_symbols

def start_websocket_thread():
    ws_thread = threading.Thread(target=async_websocket_threads)
    ws_thread.start()

def async_websocket_threads():
    asyncio.run(websocket_thread())

async def websocket_thread():
    logger.debug("Websocket Thread started")

    try:
        top_symbols = fetch_top_symbols(n=SYMBOL_NUM)
        logger.info(f"Top {SYMBOL_NUM} symbols by daily volume: {top_symbols}")

        # Start websocket loops
        await WebsocketManager().start_websockets(top_symbols, INTERVALS)
    except KeyboardInterrupt:
        logger.warning("Websocket Manager Script interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
