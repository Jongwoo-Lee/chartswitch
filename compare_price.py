from datetime import datetime

def prepare_compare(symbols, interval, data):
    prices = {symbol: {"open": None, "close": None, "high": None, "low": None} for symbol in symbols}
    
    if 'data' in data and data['data']['k']:
        
        stream = data['data']
        symbol = data['data']['s']
        event_at = datetime.fromtimestamp(stream['E']/1000)
        start_at = datetime.fromtimestamp(stream['k']['t']/1000)
        close_at = datetime.fromtimestamp(stream['k']['T']/1000)
        
        open_price = float(stream['k']['o'])
        close_price = float(stream['k']['c'])
        high_price = float(stream['k']['h'])
        low_price = float(stream['k']['l'])
        
        is_closed = stream['k']['x']
    
        if is_closed:
            print(f"{symbol} is closed {stream['k']['x']}, start at {start_at}, event at {event_at}, close at {close_at}")
            
            # Update prices
            prices[symbol]["open"] = open_price
            prices[symbol]["close"] = close_price
            prices[symbol]["high"] = high_price
            prices[symbol]["low"] = low_price
    
            print(prices)
            
            # Once both symbols have closing prices, compare changes
            if all(prices[sym]["close"] for sym in symbols):
                compare_changes(prices)


def compare_changes(prices):
    changes = {}
    for symbol, price_data in prices.items():
        if price_data["open"] and price_data["close"]:
            change = ((price_data["close"] - price_data["open"]) / price_data["open"]) * 100
            changes[symbol] = change
    
    # Assuming you want to know which symbol had a greater percentage change
    max_change_symbol = max(changes, key=changes.get)
    print(f"Symbol with the most change: {max_change_symbol} ({changes[max_change_symbol]:.2f}%)")
