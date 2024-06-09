import websockets
import json
from asyncio import Event
from util import BINANCE_WS_URL, BINANCE_STREAM_PRICE_ALL, logger, INTERVALS
from app import PriceManager

async def create_socket(stop_event: Event):
    try:
        await connect_socket_and_write(stop_event)
    
    except websockets.ConnectionClosed as e:
        if e.code == 1000:
            logger.debug("WebSocket connection closed gracefully")
        else:
            logger.error(f"WebSocket connection closed unexpectedly - {e}")
        raise

    except Exception as e:
        logger.error(f"WebSocket Unexpected Error: {e}") 
        raise

async def connect_socket_and_write(stop_event: Event):
    logger.debug(f"Starting asynchronous client for interval: {INTERVALS}")
    
    socket_url = f"{BINANCE_WS_URL}{BINANCE_STREAM_PRICE_ALL}"
    
    async with websockets.connect(socket_url) as ws:
        subscribe_message =  {
            "method": "SUBSCRIBE",
            "params": [BINANCE_STREAM_PRICE_ALL],
            "id": 1
        }

        await ws.send(json.dumps(subscribe_message))
        
        async for message in ws:
            if stop_event.is_set():
                await ws.close()
                break
            try:
                data = json.loads(message)
                PriceManager().update_price(data)
            except json.JSONDecodeError as e:
                logger.error(f"Websocket JSON Decoding Error: {e}")
                raise

        logger.debug(f"Closed websocket - {INTERVALS}")
        