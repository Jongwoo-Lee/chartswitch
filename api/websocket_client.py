import asyncio
import websocket
import websockets
import json
from config import BINANCE_WS_URL, BINANCE_WS_URL, logger
from manager import PriceManager

async def create_socket(symbols, interval, pm: PriceManager):
    logger.debug(f"Starting asynchronous client for interval: {interval}")
    combined_streams = "/".join([f"{symbol.lower()}@kline_{interval}" for symbol in symbols])
    socket_url = f"{BINANCE_WS_URL}?streams={combined_streams}"

    while True:
        try:
            async with websockets.connect(socket_url) as ws:
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
                    except websocket.WebSocketTimeoutException as e:
                        # Timeout occurred, no data received, continue to check stop_event
                        logger.warning(f"Websocket Timeout occurred: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"WebSocket error: {e}")
                        await asyncio.sleep(5)

        except websockets.ConnectionClosed as e:
            logger.warning(f"WebSocket Connection Closed: {e}. Attempting to reconnect...")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            logger.error(f"WebSocket Unexpected Error: {e}") 
            break





