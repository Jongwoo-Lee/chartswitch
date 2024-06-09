import requests
from util import logger, BINANCE_API_URL, BINANCE_24HR_TICKER, SYMBOL_NUM

def fetch_top_symbols(n=SYMBOL_NUM):
    response = requests.get(f"{BINANCE_API_URL}{BINANCE_24HR_TICKER}")
    if response.status_code == 200:
        data = response.json()
        
        # Filter symbols that end with 'USDT' and sort by quote volume
        usdt_symbols = [item for item in data if item['symbol'].endswith('USDT')]

        # Sort symbols by quote volume
        sorted_symbols = sorted(usdt_symbols, key=lambda x: float(x['quoteVolume']), reverse=True)
        top_symbols = [item['symbol'] for item in sorted_symbols[:n]]

        logger.info(f"Top {n} symbols by daily volume: {top_symbols[:5]}...")
        return top_symbols
    else:
        logger.error(f"Error fetching market data - Status code: {response.status_code}")
        return []
