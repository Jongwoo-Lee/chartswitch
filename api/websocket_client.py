import websockets
import json
from asyncio import sleep, Event
from config import BINANCE_WS_URL, BINANCE_WS_URL, logger
from app import PriceManager


async def create_socket(symbols, interval, stop_event: Event, pm: PriceManager):
    try:
        await connect_socket(symbols, interval, stop_event, pm)
    except websockets.ConnectionClosed as e:
        logger.warning(f"WebSocket Connection Closed: {e}. Attempting to reconnect...")
        await sleep(5)  # Wait before retrying
        await connect_socket(symbols, interval, stop_event, pm)
    except Exception as e:
        logger.error(f"WebSocket Unexpected Error: {e}") 

async def connect_socket(symbols, interval, stop_event, pm: PriceManager):
    logger.debug(f"Starting asynchronous client for interval: {interval}")
    
    combined_streams = "/".join([f"{symbol.lower()}@kline_{interval}" for symbol in symbols])
    socket_url = f"{BINANCE_WS_URL}?streams={combined_streams}"
    
    async with websockets.connect(socket_url) as ws:
        while not stop_event.is_set():  # Check if stop event is set

            subscribe_message =  {
                "method": "SUBSCRIBE",
                "params": [f"{symbol.lower()}@kline_{interval}" for symbol in symbols],
                "id": 1
            }

            await ws.send(json.dumps(subscribe_message))

            async for message in ws:
                try:
                    data = json.loads(message)
                    pm.update_price(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Websocket JSON Decoding Error: {e}")




