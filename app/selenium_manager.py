import time
from threading import Event
from selenium import webdriver
from app import PriceManager

def change_browser_symbol(event: Event):
    driver = webdriver.Chrome()
    last_symbol = "BTCUSDT"
    try:
        base_url = "https://www.binance.com/en/futures/"
        while not event.is_set():
            next_symbols = PriceManager().top3()

            if last_symbol != next_symbols[0]:
                last_symbol = next_symbols[0]
            else:
                last_symbol = next_symbols[1]

            full_url = base_url + last_symbol
            driver.get(full_url)

            # Simulate changing the URL periodically
            time.sleep(60)  # Change URL every few seconds
    finally:
        driver.quit()