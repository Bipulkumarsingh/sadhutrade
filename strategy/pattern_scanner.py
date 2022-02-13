import pandas as pd
import numpy as np
from src.constants import *




def levels(ohlc_day):
    """returns pivot point and support/resistance levels"""
    high = round(ohlc_day[HIGH_KEY][-1], 2)
    low = round(ohlc_day[LOW_KEY][-1], 2)
    close = round(ohlc_day[CLOSE_KEY][-1], 2)
    pivot = round((high + low + close) / 3, 2)
    r1 = round((2 * pivot - low), 2)
    r2 = round((pivot + (high - low)), 2)
    r3 = round((high + 2 * (pivot - low)), 2)
    s1 = round((2 * pivot - high), 2)
    s2 = round((pivot - (high - low)), 2)
    s3 = round((low - 2 * (high - pivot)), 2)
    return pivot, r1, r2, r3, s1, s2, s3


def trend(ohlc_df, n):
    "function to assess the trend by analyzing each candle"
    df = ohlc_df.copy()
    df["up"] = np.where(df[LOW_KEY] >= df[LOW_KEY].shift(1), 1, 0)
    df["dn"] = np.where(df[HIGH_KEY] <= df[HIGH_KEY].shift(1), 1, 0)
    if df[CLOSE_KEY][-1] > df[OPEN_KEY][-1]:
        if df["up"][-1 * n:].sum() >= 0.7 * n:
            return "uptrend"
    elif df[OPEN_KEY][-1] > df[CLOSE_KEY][-1]:
        if df["dn"][-1 * n:].sum() >= 0.7 * n:
            return "downtrend"
    else:
        return None


def res_sup(ohlc_df, ohlc_day):
    """calculates closest resistance and support levels for a given candle"""
    level = ((ohlc_df[CLOSE_KEY][-1] + ohlc_df[OPEN_KEY][-1]) / 2 + (ohlc_df[HIGH_KEY][-1] + ohlc_df[LOW_KEY][-1]) / 2) / 2
    p, r1, r2, r3, s1, s2, s3 = levels(ohlc_day)
    l_r1 = level - r1
    l_r2 = level - r2
    l_r3 = level - r3
    l_p = level - p
    l_s1 = level - s1
    l_s2 = level - s2
    l_s3 = level - s3
    lev_ser = pd.Series([l_p, l_r1, l_r2, l_r3, l_s1, l_s2, l_s3], index=["p", "r1", "r2", "r3", "s1", "s2", "s3"])
    sup = lev_ser[lev_ser > 0].idxmin()
    res = lev_ser[lev_ser < 0].idxmax()
    print(res, '\n', sup)
    return eval('{}'.format(res)), eval('{}'.format(sup))


def candle_type(ohlc_df):
    """returns the candle type of the last candle of an OHLC DF"""
    candle = None
    if doji(ohlc_df)["doji"][-1] == True:
        candle = "doji"
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_green":
        candle = "maru_bozu_green"
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_red":
        candle = "maru_bozu_red"
    if shooting_star(ohlc_df)["sstar"][-1] == True:
        candle = "shooting_star"
    if hammer(ohlc_df)["hammer"][-1] == True:
        candle = "hammer"
    return candle


def candle_pattern(ohlc_df, ohlc_day):
    """returns the candle pattern identified"""
    pattern = None
    signi = LOW_KEY
    avg_candle_size = abs(ohlc_df[CLOSE_KEY] - ohlc_df[OPEN_KEY]).median()
    sup, res = res_sup(ohlc_df, ohlc_day)

    if (sup - 1.5 * avg_candle_size) < ohlc_df[CLOSE_KEY][-1] < (sup + 1.5 * avg_candle_size):
        signi = "HIGH"

    if (res - 1.5 * avg_candle_size) < ohlc_df[CLOSE_KEY][-1] < (res + 1.5 * avg_candle_size):
        signi = "HIGH"

    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df[CLOSE_KEY][-1] > ohlc_df[CLOSE_KEY][-2] \
            and ohlc_df[CLOSE_KEY][-1] > ohlc_df[OPEN_KEY][-1]:
        pattern = "doji_bullish"

    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df[CLOSE_KEY][-1] < ohlc_df[CLOSE_KEY][-2] \
            and ohlc_df[CLOSE_KEY][-1] < ohlc_df[OPEN_KEY][-1]:
        pattern = "doji_bearish"

    if candle_type(ohlc_df) == "maru_bozu_green":
        pattern = "maru_bozu_bullish"

    if candle_type(ohlc_df) == "maru_bozu_red":
        pattern = "maru_bozu_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" and candle_type(ohlc_df) == "hammer":
        pattern = "hanging_man_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" and candle_type(ohlc_df) == "hammer":
        pattern = "hammer_bullish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" and candle_type(ohlc_df) == "shooting_star":
        pattern = "shooting_star_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" \
            and candle_type(ohlc_df) == "doji" \
            and ohlc_df[HIGH_KEY][-1] < ohlc_df[CLOSE_KEY][-2] \
            and ohlc_df[LOW_KEY][-1] > ohlc_df[OPEN_KEY][-2]:
        pattern = "harami_cross_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) == "doji" \
            and ohlc_df[HIGH_KEY][-1] < ohlc_df[OPEN_KEY][-2] \
            and ohlc_df[LOW_KEY][-1] > ohlc_df[CLOSE_KEY][-2]:
        pattern = "harami_cross_bullish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df[OPEN_KEY][-1] > ohlc_df[HIGH_KEY][-2] \
            and ohlc_df[CLOSE_KEY][-1] < ohlc_df[LOW_KEY][-2]:
        pattern = "engulfing_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df[CLOSE_KEY][-1] > ohlc_df[HIGH_KEY][-2] \
            and ohlc_df[OPEN_KEY][-1] < ohlc_df[LOW_KEY][-2]:
        pattern = "engulfing_bullish"

    return "Significance - {}, Pattern - {}".format(signi, pattern)


##############################################################################################

# def main():
#     for ticker in tickers:
#         try:
#             ohlc = fetchOHLC(ticker, '5minute', 5)
#             ohlc_day = fetchOHLC(ticker, 'day', 30)
#             ohlc_day = ohlc_day.iloc[:-1, :]
#             cp = candle_pattern(ohlc, ohlc_day)
#             print(ticker, ": ", cp)
#         except:
#             print("skipping for ", ticker)


# # Continuous execution
# starttime = time.time()
# timeout = time.time() + 60 * 60 * 1  # 60 seconds times 60 meaning the script will run for 1 hr
# while time.time() <= timeout:
#     try:
#         print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#         main()
#         time.sleep(300 - ((time.time() - starttime) % 300.0))  # 300 second interval between each new execution
#     except KeyboardInterrupt:
#         print('\n\nKeyboard exception received. Exiting.')
#         exit()
