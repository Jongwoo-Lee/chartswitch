import pandas as pd
from threading import Lock

class PriceManager:
    _instance = None
    _lock = Lock()  # Class-level lock
    _is_initialized = False  # Flag to check if the instance has been initialized

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(PriceManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not self.__class__._is_initialized:
            print("Price manager: initializing the price data DataFrame.")
            self.price_data = pd.DataFrame(columns=[
                'symbol', 'interval', 'event_ts', 'open_ts', 'close_ts', 
                'open_price', 'close_price', 'high_price', 'low_price', 
                'is_closed'])
            
            self.price_data['is_closed'] = self.price_data['is_closed'].astype(bool)
            self.__class__._is_initialized = True  # Set the flag indicating initialization is done

    def update_price(self, data):
        with self._lock: 
            if 'data' in data and 'k' in data['data']:
                stream = data['data']
                symbol = stream['s']
                interval = stream['k']['i']

                event_ts = pd.to_datetime(stream['E'], unit='ms')
                start_ts = pd.to_datetime(stream['k']['t'], unit='ms')
                close_ts = pd.to_datetime(stream['k']['T'], unit='ms')

                open_price = float(stream['k']['o'])
                close_price = float(stream['k']['c'])
                high_price = float(stream['k']['h'])
                low_price = float(stream['k']['l'])
                
                is_closed = stream['k']['x']

                new_entry = {
                    'symbol': symbol, 'interval': interval,
                    'event_ts': event_ts, 'open_ts': start_ts, 'close_ts': close_ts, 
                    'open_price': open_price, 'close_price': close_price, 'high_price': high_price, 'low_price': low_price, 
                    'is_closed': is_closed
                }

                self.price_data = pd.concat([self.price_data, pd.DataFrame([new_entry])], ignore_index=True)
                print(f"Price manager: updated price data for {symbol} with interval {interval} at {event_ts}.")

    def partial_cleanup(self):
        # Keeps only the last 'hours' of data for the specified interval.
        threshold = pd.to_datetime('now') - pd.Timedelta(hours=1)
        self.price_data = self.price_data[(self.price_data['event_ts'] > threshold) | (self.price_data['interval'] != "1m")]

    def compare_most_recent_prices(self):
        if not self.price_data.empty:
            recent_prices = self.price_data.groupby(['symbol', 'interval']).apply(lambda x: x.iloc[-1])
            return recent_prices
        else:
            return pd.DataFrame()  # Return an empty DataFrame if there's no data
        
    def cleanup(self):
        # Implement cleanup logic here, such as closing connections
        print("Price manager: cleaning up.")
        print("Price manager: clean up done.")
        pass