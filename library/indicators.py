import numpy as np
from stocktrends import Renko


def atr(df, n):
    """function to calculate True Range and Average True Range"""
    df = df.copy()
    df['H-L'] = abs(df['high'] - df['low'])
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()
    # df['ATR'] = df['TR'].rolling(com=n,min_periods=n).mean()
    return df['ATR']


def MACD(df, a, b, c):
    """function to calculate MACD
       typical values a(fast moving average) = 12;
                      b(slow moving average) =26;
                      c(signal line ma window) =9"""
    df = df.copy()
    df["MA_Fast"] = df["close"].ewm(span=a, min_periods=a).mean()
    df["MA_Slow"] = df["close"].ewm(span=b, min_periods=b).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=c, min_periods=c).mean()
    df.dropna(inplace=True)
    return df


def bollBnd(df, n):
    """Function to calculate Bollinger Band"""
    df = df.copy()
    df["MA"] = df['close'].rolling(n).mean()
    # df["MA"] = df['close'].ewm(span=n,min_periods=n).mean()
    df["BB_up"] = df["MA"] + 2 * df['close'].rolling(n).std(
        ddof=0)  # ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2 * df['close'].rolling(n).std(
        ddof=0)  # ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


def rsi(df, n):
    """Function to calculate RSI"""
    delta = df["close"].diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[n - 1]] = np.mean(u[:n])  # first value is average of gains
    u = u.drop(u.index[:(n - 1)])
    d[d.index[n - 1]] = np.mean(d[:n])  # first value is average of losses
    d = d.drop(d.index[:(n - 1)])
    rs = u.ewm(com=n, min_periods=n).mean() / d.ewm(com=n, min_periods=n).mean()
    return 100 - 100 / (1 + rs)


def adx(df, n):
    """function to calculate ADX"""
    df2 = df.copy()
    df2['H-L'] = abs(df2['high'] - df2['low'])
    df2['H-PC'] = abs(df2['high'] - df2['close'].shift(1))
    df2['L-PC'] = abs(df2['low'] - df2['close'].shift(1))
    df2['TR'] = df2[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df2['DMplus'] = np.where((df2['high'] - df2['high'].shift(1)) > (df2['low'].shift(1) - df2['low']),
                             df2['high'] - df2['high'].shift(1), 0)
    df2['DMplus'] = np.where(df2['DMplus'] < 0, 0, df2['DMplus'])
    df2['DMminus'] = np.where((df2['low'].shift(1) - df2['low']) > (df2['high'] - df2['high'].shift(1)),
                              df2['low'].shift(1) - df2['low'], 0)
    df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i - 1] - (TRn[i - 1] / n) + TR[i])
            DMplusN.append(DMplusN[i - 1] - (DMplusN[i - 1] / n) + DMplus[i])
            DMminusN.append(DMminusN[i - 1] - (DMminusN[i - 1] / n) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN'] = 100 * (df2['DMplusN'] / df2['TRn'])
    df2['DIminusN'] = 100 * (df2['DMminusN'] / df2['TRn'])
    df2['DIdiff'] = abs(df2['DIplusN'] - df2['DIminusN'])
    df2['DIsum'] = df2['DIplusN'] + df2['DIminusN']
    df2['DX'] = 100 * (df2['DIdiff'] / df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2 * n - 1:
            ADX.append(np.NaN)
        elif j == 2 * n - 1:
            ADX.append(df2['DX'][j - n + 1:j + 1].mean())
        elif j > 2 * n - 1:
            ADX.append(((n - 1) * ADX[j - 1] + DX[j]) / n)
    df2['ADX'] = np.array(ADX)
    return df2['ADX']


def super_trend(df, n, m):
    """function to calculate Super trend given historical candle data
        n = n day ATR - usually 7 day ATR is used
        m = multiplier - usually 2 or 3 is used"""
    df = df.copy()
    df['ATR'] = atr(df, n)
    df["B-U"] = ((df['high'] + df['low']) / 2) + m * df['ATR']
    df["B-L"] = ((df['high'] + df['low']) / 2) - m * df['ATR']
    df["U-B"] = df["B-U"]
    df["L-B"] = df["B-L"]
    ind = df.index
    for i in range(n, len(df)):
        if df['close'][i - 1] <= df['U-B'][i - 1]:
            df.loc[ind[i], 'U-B'] = min(df['B-U'][i], df['U-B'][i - 1])
        else:
            df.loc[ind[i], 'U-B'] = df['B-U'][i]
    for i in range(n, len(df)):
        if df['close'][i - 1] >= df['L-B'][i - 1]:
            df.loc[ind[i], 'L-B'] = max(df['B-L'][i], df['L-B'][i - 1])
        else:
            df.loc[ind[i], 'L-B'] = df['B-L'][i]
    df['s_trend'] = np.nan
    test = 0
    for test in range(n, len(df)):
        if df['close'][test - 1] <= df['U-B'][test - 1] and df['close'][test] > df['U-B'][test]:
            df.loc[ind[test], 's_trend'] = df['L-B'][test]
            break
        if df['close'][test - 1] >= df['L-B'][test - 1] and df['close'][test] < df['L-B'][test]:
            df.loc[ind[test], 's_trend'] = df['U-B'][test]
            break
    for i in range(test + 1, len(df)):
        if df['s_trend'][i - 1] == df['U-B'][i - 1] and df['close'][i] <= df['U-B'][i]:
            df.loc[ind[i], 's_trend'] = df['U-B'][i]
        elif df['s_trend'][i - 1] == df['U-B'][i - 1] and df['close'][i] >= df['U-B'][i]:
            df.loc[ind[i], 's_trend'] = df['L-B'][i]
        elif df['s_trend'][i - 1] == df['L-B'][i - 1] and df['close'][i] >= df['L-B'][i]:
            df.loc[ind[i], 's_trend'] = df['L-B'][i]
        elif df['s_trend'][i - 1] == df['L-B'][i - 1] and df['close'][i] <= df['L-B'][i]:
            df.loc[ind[i], 's_trend'] = df['U-B'][i]
    return df['s_trend']


def renko_df(df):
    """function to convert ohlc data into renko bricks"""
    df = df.copy()
    df.reset_index(inplace=True)
    df2 = Renko(df)
    df2.brick_size = 10
    renko_data = df2.get_ohlc_data()
    return renko_data


def obv(df_data):
    """function to calculate On Balance Volume"""

    daily_ret_key = "daily_ret"
    direction_key = "direction"
    volume_adjusted_key = "vol_adj"

    df_data[daily_ret_key] = df_data["Close"].pct_change()
    df_data[direction_key] = np.where(df_data[daily_ret_key] >= 0, 1, -1)
    df_data.iloc[0].at[direction_key] = 0
    df_data[volume_adjusted_key] = df_data["Volume"] * df_data[direction_key]
    df_data["obv"] = df_data[volume_adjusted_key].cumsum()
    return df_data
