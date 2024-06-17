import threading
import signal
from util import logger
from app import WebsocketManager, PriceManager, WindowManager, SeleniumManager

def signal_handler(sig, frame):
    logger.info(f"Signal {sig} received. Shutting down gracefully...")
    close_all()
    
def close_all():
    SeleniumManager().cleanup()
    WindowManager().cleanup()
    WebsocketManager().cleanup()

def start_threads():
    import api
    
    # Register the cleanup functions to be called on exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    symbols = api.fetch_top_symbols()
    PriceManager().reset_symbols(symbols)
    
    ws_thread = start_websocket_thread()
    sl_thread = start_selenium_thread()

    # Tkinter has to be in main thread
    try:
        WindowManager().start_window()
    except KeyboardInterrupt:
        logger.debug("Keyboard Interrupt - Start closing application")
    
    sl_thread.join()
    logger.debug("Selenium thread closed")
    ws_thread.join()
    logger.debug("Websocket thread closed")


def start_websocket_thread():
    ws_thread = threading.Thread(target=run_async_websocket)
    ws_thread.start()
    return ws_thread

def start_selenium_thread():
    sm = SeleniumManager()
    sl_thread = threading.Thread(target=sm.change_browser_symbol)
    sl_thread.start()
    return sl_thread

def run_async_websocket():
    import asyncio
    asyncio.run(init_wsm())

async def init_wsm():
    # Start websocket loops
    await WebsocketManager().start_websockets()