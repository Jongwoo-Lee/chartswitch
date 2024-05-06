import pandas as pd
from config import logger

class PriceManager:
    _instance = None
    _is_initialized = False  # Flag to check if the instance has been initialized

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PriceManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Price manager: initializing the price DataFrame.")
            self.price_data = pd.DataFrame(columns=[
                'symbol', 'interval', 'event_ts', 'open_ts', 'close_ts', 
                'open_price', 'close_price', 'high_price', 'low_price', 
                'is_closed'])
            
            self.price_data['is_closed'] = self.price_data['is_closed'].astype(bool)
            self.__class__._is_initialized = True  # Set the flag indicating initialization is done

    def update_price(self, data):
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

            new_df = pd.DataFrame([{
                'symbol': symbol, 'interval': interval,
                'event_ts': event_ts, 'open_ts': start_ts, 'close_ts': close_ts, 
                'open_price': open_price, 'close_price': close_price, 'high_price': high_price, 'low_price': low_price, 
                'is_closed': is_closed
            }])

            if self.price_data.empty:
                self.price_data = new_df
            else:
                self.price_data = pd.concat([self.price_data, new_df], ignore_index=True)

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
        self.price_data = None
        logger.debug("Price manager: clean up done.")
        pass