from library.candlesticks import *
from library.price_action import *


def candle_type(ohlc_df):
    """returns the candle type of the last candle of an OHLC DF"""
    candle = None
    if doji(ohlc_df)["doji"][-1]:
        candle = "doji"
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_green":
        candle = "maru_bozu_green"
    if maru_bozu(ohlc_df)["maru_bozu"][-1] == "maru_bozu_red":
        candle = "maru_bozu_red"
    if shooting_star(ohlc_df)["sstar"][-1]:
        candle = "shooting_star"
    if hammer(ohlc_df)["hammer"][-1]:
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
