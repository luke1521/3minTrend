import pandas as pd
from binance.um_futures import UMFutures
import datetime
import time
import numpy as np
import math
import requests

um_futures_client = UMFutures()
time_start_date = datetime.datetime.now() - datetime.timedelta(minutes=1500)
time_start_second = int(time_start_date.timestamp()) * 1000


def get_tradeable_symbols():
    ticker_list = []
    symbols = um_futures_client.exchange_info()["symbols"]
    for sym in symbols:
        if sym["quoteAsset"] == "USDT" and sym["status"] == "TRADING":
            ticker_list.append(sym["symbol"])
    return ticker_list


def get_kline(ticker):
    price = um_futures_client.klines(symbol=ticker, interval="3m", startTime=time_start_second)
    time.sleep(0.1)
    if len(price) != 500:
        return []
    return price


def get_ema(kline, length):
    df = pd.DataFrame(kline)
    ema = df.ewm(span=length, min_periods=length, adjust=False).mean()
    ema_list = ema.values.tolist()
    return ema_list


def extract_close_price(ticker_kline):
    close_price = []
    for price_values in ticker_kline:
        if math.isnan(float(price_values[4])):
            return []
        close_price.append(float(price_values[4]))
    return close_price


def get_up_trend(kline):
    uptrend_tickers = []
    downtrend_tickers = []
    for ticker in kline.keys():
        close = extract_close_price(kline[ticker])
        ema180 = get_ema(close, 180)[-100:]
        ema180 = [item for sublist in ema180 for item in sublist]
        close100 = extract_close_price(kline[ticker])[-100:]
        ema180np = np.array(ema180)
        close100np = np.array(close100)
        if np.all(ema180np < close100np):
            uptrend_tickers.append(ticker)
        if np.all(ema180np > close100np):
            downtrend_tickers.append(ticker)
    return uptrend_tickers, downtrend_tickers


def send_telegram_message(message):
    telegram_token = "6175801430:AAFKr7osgB7s36HhAI2Drhtbhgq_eSvaPZ0"
    telegram_id = "1235292983"
    api = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_id}&parse_mode=MarkdownV2&text={message}"
    res = requests.get(api)
    if res.status_code == 200:
        return "Telegram message sent"
    else:
        return "Telegram send failed"
