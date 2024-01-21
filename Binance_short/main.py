import func
import json
import time
from datetime import datetime


def step1():
    tradeable_tickers = func.get_tradeable_symbols()
    counts = 0
    kline_info_dict = {}
    print("Gathering kline info...")
    for ticker in tradeable_tickers:
        counts += 1
        kline_info = func.get_kline(ticker)
        if (len(kline_info)) > 0:
            kline_info_dict[ticker] = kline_info
            # counts += 1
    print(f"{counts} items stored")
    # else:
    #     print(f"{counts} items is not stored")

    if len(kline_info_dict) > 0:
        with open("1_kline_info.json", "w") as fp:
            json.dump(kline_info_dict, fp, indent=4)
        print("kline saved successfully.")


def step2():
    with (open("1_kline_info.json") as json_file):
        kline_info = json.load(json_file)
        uptrend_tickers, downtrend_tickers = func.get_up_trend(kline_info)

        old_uptrend_tickers = []
        old_downtrend_tickers = []

        # comment out this block on first run
        with open("1_result.json") as json_file2:
            old_result = json.load(json_file2)
            for ticker in old_result["uptrend_tickers"]:
                old_uptrend_tickers.append(ticker)
            for ticker in old_result["downtrend_tickers"]:
                old_downtrend_tickers.append(ticker)

        uptrend_list_new = list(set(uptrend_tickers) - set(old_uptrend_tickers))
        downtrend_list_new = list(set(downtrend_tickers) - set(old_downtrend_tickers))

        print("Up_Trend3: " + str(uptrend_tickers), "\n" "Up_Trend3_New: " + str(uptrend_list_new))
        print("Down_Trend3: " + str(downtrend_tickers), "\n" "Down_Trend3_New: " + str(downtrend_list_new))

        message = "New Up Trend:  " + "*" + str(uptrend_list_new).replace("[", "").replace(
                    "]", "").replace(",", " ").replace(
                    "'", "") + "*" + "\n" + "New Down Trend:  " + "*" + str(downtrend_list_new).replace(
                    "[", "").replace("]", "").replace(
                    ",", " ").replace("'", "") + "*"
        print(message)
        if len(uptrend_list_new) > 0 or len(downtrend_list_new):
            telegram_message = func.send_telegram_message(message)
            print(telegram_message)

        result = {
            "uptrend_tickers": uptrend_tickers,
            "downtrend_tickers": downtrend_tickers
        }
        with open("1_result.json", "w") as fp:
            json.dump(result, fp, indent=4)


if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    start = time.time()
    print(current_time)
    step1()
    step2()
    end = time.time()
    print(f"duration: {end - start}")
