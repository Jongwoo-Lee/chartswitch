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
        if 'data' in data and 'k' in data['data']:
            new_series = self.make_price_series(data['data'])
            new_series = self.calculate_price_change(new_series)
            

    def make_price_series(self, stream):
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

        new_series = pd.Series({
                'symbol': symbol, 'interval': interval,
                'event_ts': event_ts, 'open_ts': start_ts, 'close_ts': close_ts, 
                'open_price': open_price, 'close_price': close_price, 'high_price': high_price, 'low_price': low_price, 
                'is_closed': is_closed, 'pct_change': 0, 'abs_pct_change': 0, 'rolling_sum': 0
            })

        return new_series

    def calculate_price_change(self, series: pd.Series):
        if 'symbol' in series.index and pd.notna(series['symbol']) and 'close_price' in series.index and pd.notna(series['close_price']):
            symbol = series['symbol']
            close_price = series['close_price']
            previous_price = self.previous_prices[symbol]
            pct_change, abs_pct_change = 0, 0

            if previous_price is not None:
                pct_change = (close_price - previous_price) / previous_price
                abs_pct_change = abs(pct_change)

                if len(self.price_deques_100[symbol]) == self.price_deques_100[symbol].maxlen :
                    self.rolling_sums[symbol] -= self.price_deques_100[symbol][0]

                self.rolling_sums[symbol] += abs_pct_change
                self.price_deques_100[symbol].append(abs_pct_change)

            self.previous_prices[symbol] = close_price
            series['pct_change'] = pct_change
            series['abs_pct_change'] = abs_pct_change
            series['rolling_sum'] = self.rolling_sums[symbol]

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