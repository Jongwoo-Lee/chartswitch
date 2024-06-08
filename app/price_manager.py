import pandas as pd
from util import logger
from collections import deque

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

            # Initialize state dictionaries
            self.rolling_sums = {}
            self.price_deques_100 = {}
            self.previous_prices = {}

            self.__class__._is_initialized = True  # Set the flag indicating initialization is done
    
    def update_price(self, data):
        if 'data' in data and isinstance(data['data'], list):
            for symbol_info in data['data']:
                if 's' in symbol_info and 'i' in symbol_info:
                    price_dict = self.make_price_dict(symbol_info)
                    price_dict = self.calculate_price_change(price_dict)
            

    def make_price_dict(self, stream):
        symbol = stream['s']
        event_ts = pd.to_datetime(stream['E'], unit='ms')
        index_price = float(stream['i'])
        
        price_dict = {
                'symbol': symbol, 'event_ts': event_ts, 'index_price': index_price, 
                'pct_change': 0, 'abs_pct_change': 0, 'rolling_sum': 0
            }
        return price_dict

    def calculate_price_change(self, series: dict):
        if 'symbol' in series and 'index_price' in series:
            symbol = series['symbol']
            index_price = series['index_price']

            if symbol in self.previous_prices and symbol in self.price_deques_100 and symbol in self.rolling_sums:
                previous_price = self.previous_prices[symbol]
                pct_change, abs_pct_change = 0, 0

                if previous_price is not None:
                    pct_change = (index_price - previous_price) / previous_price
                    abs_pct_change = abs(pct_change)

                    if len(self.price_deques_100[symbol]) == self.price_deques_100[symbol].maxlen :
                        self.rolling_sums[symbol] -= self.price_deques_100[symbol][0]

                    self.rolling_sums[symbol] += abs_pct_change
                    self.price_deques_100[symbol].append(abs_pct_change)

                self.previous_prices[symbol] = index_price

        return series 

    def reset_symbols(self, symbols):
        for symbol in symbols:
            self.rolling_sums[symbol] = 0
            self.price_deques_100[symbol] = deque(maxlen=100)
            self.previous_prices[symbol] = None

        return symbols

    def cleanup(self):
        # Implement cleanup logic here, such as closing connections
        self.rolling_sums = None
        self.price_deques_100 = None
        self.previous_prices = None
        logger.debug("Price manager: clean up done.")
        pass