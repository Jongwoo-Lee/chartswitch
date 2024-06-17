import time
from selenium import webdriver

from util import logger

class SeleniumManager:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SeleniumManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Initializing Selenium Manager")

            self.driver = webdriver.Chrome()
            self.is_open = True

            self.__class__._is_initialized = True     

    def change_browser_symbol(self):
        from app import PriceManager
        last_symbol = "BTCUSDT"
        try:
            base_url = "https://www.binance.com/en/futures/"
            
            while self.is_open:
                next_symbols = PriceManager().top4()

                if last_symbol != next_symbols[0]:
                    last_symbol = next_symbols[0]
                else:
                    last_symbol = next_symbols[1]

                full_url = base_url + last_symbol

                self.driver.get(full_url)

                # Simulate changing the URL periodically
                time.sleep(60)  # Change URL every few seconds
        except Exception as e:
            logger.error(f"Selenium error: {e}")
        finally:
            self.driver.quit()

    def cleanup(self):
        self.is_open = False