import websockets
import json
from asyncio import Event
from config import BINANCE_WS_URL, BINANCE_WS_URL, logger
from app import PriceManager


async def create_socket(symbols, interval, stop_event: Event, pm: PriceManager):
    try:
        await connect_socket_and_write(symbols, interval, stop_event, pm)
    
    except websockets.ConnectionClosed as e:
        if e.code == 1000:
            logger.debug("WebSocket connection closed gracefully")
        else:
            logger.error(f"WebSocket connection closed unexpectedly - {e}")
        raise

    except Exception as e:
        logger.error(f"WebSocket Unexpected Error: {e}") 
        raise

async def connect_socket_and_write(symbols, interval, stop_event: Event, pm: PriceManager):
    logger.debug(f"Starting asynchronous client for interval: {interval}")
    
    combined_streams = "/".join([f"{symbol.lower()}@kline_{interval}" for symbol in symbols])
    socket_url = f"{BINANCE_WS_URL}?streams={combined_streams}"
    
    async with websockets.connect(socket_url) as ws:
        subscribe_message =  {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@kline_{interval}" for symbol in symbols],
            "id": 1
        }

        await ws.send(json.dumps(subscribe_message))

        async for message in ws:
            if stop_event.is_set():
                await ws.close()
            try:
                data = json.loads(message)
                pm.update_price(data)
            except json.JSONDecodeError as e:
                logger.error(f"Websocket JSON Decoding Error: {e}")
                raise

        logger.debug(f"Closed websocket - {interval} interval")
        