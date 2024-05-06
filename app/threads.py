import threading
import asyncio

from config import logger, SYMBOL_NUM, INTERVALS
from app import WebsocketManager, PriceManager
from api import fetch_top_symbols


def start_websocket_thread(event: threading.Event):
    ws_thread = threading.Thread(target=run_websocket, args=(event,))
    ws_thread.start()
    return ws_thread

def run_websocket(event: threading.Event):
    asyncio.run(websocket_loop())

    # Rest of the clean up after websocket thread
    event.set()

async def websocket_loop():
    # Start websocket loops
    await WebsocketManager().start_websockets(
        fetch_top_symbols(n=SYMBOL_NUM), 
        INTERVALS
    )