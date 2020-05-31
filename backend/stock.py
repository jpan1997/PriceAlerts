import requests
import threading

FINNHUB_API_KEY = 'br9dmhnrh5rbhn690ecg'


def get_stock_price(ticker):
    r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + \
                     '&token=' + FINNHUB_API_KEY)
    # TODO: input sanitization
    if r.status_code == 200:  # 429 if exceed api limit
        return r.json()['pc']
    else:
        return None


def update_stock_prices(alert_manager):
    for ticker in alert_manager.get_stock_list():
        alert_manager.update_price(ticker, get_stock_price(ticker))


def run(alert_manager):
    print("server thread running")
    ticker = threading.Event()
    while not ticker.wait(1):
        update_stock_prices(alert_manager)
