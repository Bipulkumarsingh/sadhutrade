import numpy as np
from src.constants import CLOSE_KEY, OPEN_KEY, HIGH_KEY, LOW_KEY


def doji(ohlc_df):
    """returns dataframe with doji candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df[CLOSE_KEY] - df[OPEN_KEY]).median()
    df["doji"] = abs(df[CLOSE_KEY] - df[OPEN_KEY]) <= (0.05 * avg_candle_size)
    return df


def maru_bozu(ohlc_df):
    """returns dataframe with maru bozu candle column"""
    df = ohlc_df.copy()
    avg_candle_size = abs(df[CLOSE_KEY] - df[OPEN_KEY]).median()
    df["h-c"] = df[HIGH_KEY] - df[CLOSE_KEY]
    df["l-o"] = df[LOW_KEY] - df[OPEN_KEY]
    df["h-o"] = df[HIGH_KEY] - df[OPEN_KEY]
    df["l-c"] = df[LOW_KEY] - df[CLOSE_KEY]
    df["maru_bozu"] = np.where((df[CLOSE_KEY] - df[OPEN_KEY] > 2 * avg_candle_size) &
                               (df[["h-c", "l-o"]].max(axis=1) < 0.005 * avg_candle_size), "maru_bozu_green",
                               np.where((df[OPEN_KEY] - df[CLOSE_KEY] > 2 * avg_candle_size) &
                                        (abs(df[["h-o", "l-c"]]).max(axis=1) < 0.005 * avg_candle_size),
                                        "maru_bozu_red", False))
    df.drop(["h-c", "l-o", "h-o", "l-c"], axis=1, inplace=True)
    return df


def hammer(ohlc_df):
    """returns dataframe with hammer candle column"""
    df = ohlc_df.copy()
    df["hammer"] = (((df[HIGH_KEY] - df[LOW_KEY]) > 3 * (df[OPEN_KEY] - df[CLOSE_KEY])) &
                    ((df[CLOSE_KEY] - df[LOW_KEY]) / (.001 + df[HIGH_KEY] - df[LOW_KEY]) > 0.6) &
                    ((df[OPEN_KEY] - df[LOW_KEY]) / (.001 + df[HIGH_KEY] - df[LOW_KEY]) > 0.6)) & \
                   (abs(df[CLOSE_KEY] - df[OPEN_KEY]) > 0.1 * (df[HIGH_KEY] - df[LOW_KEY]))
    return df


def shooting_star(ohlc_df):
    """returns dataframe with shooting star candle column"""
    df = ohlc_df.copy()
    df["sstar"] = (((df[HIGH_KEY] - df[LOW_KEY]) > 3 * (df[OPEN_KEY] - df[CLOSE_KEY])) &
                   ((df[HIGH_KEY] - df[CLOSE_KEY]) / (.001 + df[HIGH_KEY] - df[LOW_KEY]) > 0.6) &
                   ((df[HIGH_KEY] - df[OPEN_KEY]) / (.001 + df[HIGH_KEY] - df[LOW_KEY]) > 0.6)) & \
                  (abs(df[CLOSE_KEY] - df[OPEN_KEY]) > 0.1 * (df[HIGH_KEY] - df[LOW_KEY]))
    return df
