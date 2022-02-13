import numpy as np
import pandas as pd
import statsmodels.api as sm


def levels(ohlc_day):
    """returns pivot point and support/resistance levels"""
    high = round(ohlc_day["high"][-1], 2)
    low = round(ohlc_day["low"][-1], 2)
    close = round(ohlc_day["close"][-1], 2)
    pivot = round((high + low + close) / 3, 2)
    r1 = round((2 * pivot - low), 2)
    r2 = round((pivot + (high - low)), 2)
    r3 = round((high + 2 * (pivot - low)), 2)
    s1 = round((2 * pivot - high), 2)
    s2 = round((pivot - (high - low)), 2)
    s3 = round((low - 2 * (high - pivot)), 2)
    return pivot, r1, r2, r3, s1, s2, s3


def trend(ohlc_df, n):
    """function to assess the trend by analyzing each candle"""
    df = ohlc_df.copy()
    df["up"] = np.where(df["low"] >= df["low"].shift(1), 1, 0)
    df["dn"] = np.where(df["high"] <= df["high"].shift(1), 1, 0)
    if df["close"][-1] > df["open"][-1]:
        if df["up"][-1 * n:].sum() >= 0.7 * n:
            return "uptrend"
    elif df["open"][-1] > df["close"][-1]:
        if df["dn"][-1 * n:].sum() >= 0.7 * n:
            return "downtrend"
    else:
        return None


def slope(ohlc_df, n):
    """function to calculate the slope of regression line for n consecutive points on a plot"""
    df = ohlc_df.iloc[-1 * n:, :]
    y = ((df["open"] + df["close"]) / 2).values
    x = np.array(range(n))
    y_scaled = (y - y.min()) / (y.max() - y.min())
    x_scaled = (x - x.min()) / (x.max() - x.min())
    x_scaled = sm.add_constant(x_scaled)
    model = sm.OLS(y_scaled, x_scaled)
    results = model.fit()
    slope_angle = np.rad2deg(np.arctan(results.params[-1]))
    return slope_angle


def res_sup(ohlc_df, ohlc_day):
    """calculates closest resistance and support levels for a given candle"""
    level = ((ohlc_df["close"][-1] + ohlc_df["open"][-1]) / 2 + (ohlc_df["high"][-1] + ohlc_df["low"][-1]) / 2) / 2
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
    return eval('{}'.format(res)), eval('{}'.format(sup))
