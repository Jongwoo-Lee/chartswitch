import threading
import asyncio

from app import WebsocketManager, PriceManager, WindowManager

def start_threads():
    import api

    stop_event = threading.Event()

    symbols = api.fetch_top_symbols()
    PriceManager().reset_symbols(symbols)
    
    start_websocket_thread(stop_event)
    start_selenium_thread(stop_event)

    return stop_event

def start_websocket_thread(event: threading.Event):
    ws_thread = threading.Thread(target=run_websocket, args=(event,))
    ws_thread.start()
    return ws_thread

def start_selenium_thread(event: threading.Event):
    from app import change_browser_symbol
    sl_thread = threading.Thread(target=change_browser_symbol, args=(event,))
    sl_thread.start()
    return sl_thread

def run_websocket(event: threading.Event):
    asyncio.run(init_wsm())

    # Rest of the clean up after websocket thread
    event.set()
    WindowManager().cleanup()

async def init_wsm():
    # Start websocket loops
    await WebsocketManager().start_websockets()