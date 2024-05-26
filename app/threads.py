import threading
import asyncio

from app import WebsocketManager 
from api import fetch_top_symbols

def start_websocket_thread(event: threading.Event):
    ws_thread = threading.Thread(target=run_websocket, args=(event,))
    ws_thread.start()
    return ws_thread

def run_websocket(event: threading.Event):
    asyncio.run(websocket_loop())

    # Rest of the clean up after websocket thread
    print("rest of the clean up")
    event.set()

async def websocket_loop():

    symbols = fetch_top_symbols(4)
    # Start websocket loops
    await WebsocketManager().start_websockets(symbols)