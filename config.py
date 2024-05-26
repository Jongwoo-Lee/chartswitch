import logging

BINANCE_24HR_TICKER_API = "https://fapi.binance.com/fapi/v1/ticker/24hr"
BINANCE_WS_URL = "wss://stream.binance.com:9443/stream"

SYMBOL_NUM = 2
INTERVALS = ["1m"] # ["1m","5m","15m","1h","4h","1d"]
UPDATE_INTERVAL = 3600  # 1 hour in seconds

# Configure the logging system
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(funcName)s : %(message)s",
    filename="app.log",
    filemode="a"
)

# Create a logger object
logger = logging.getLogger("chartswitch")
