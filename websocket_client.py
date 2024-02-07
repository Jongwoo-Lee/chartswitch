import websocket
import json
from config import BINANCE_WS_URL, BINANCE_WS_URL
from manager.price_manager import PriceManager

def create_socket(symbols, interval, stop_event):
    print(f"Starting thread for interval: {interval}")
    pm = PriceManager()

    combined_streams = "/".join([f"{symbol.lower()}@kline_{interval}" for symbol in symbols])
    socket_url = f"{BINANCE_WS_URL}?streams={combined_streams}"

    # Create a WebSocket object without using WebSocketApp
    ws = websocket.create_connection(socket_url)
    
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [f"{symbol.lower()}@kline_{interval}" for symbol in symbols],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

    # Main loop to handle WebSocket messages
    while not stop_event.is_set():
        try:
            # Receive WebSocket message with a timeout
            result = ws.recv()
            if result:
                data = json.loads(result)
                pm.update_price(data)

        except websocket.WebSocketTimeoutException as e:
            # Timeout occurred, no data received, continue to check stop_event
            print(f"Timeout occurred: {e}")
            continue
        except Exception as e:
            print(f"WebSocket error: {e}")
            break

        # Check if stop_event is set
        if stop_event.is_set():
            print("Stop event detected, closing WebSocket")
            break

    # Close WebSocket connection
    ws.close()
    print(f"Stopping thread for interval: {interval}")
