import time
import datasource.smartapi
from library.candlesticks import *
# from library.indicators import *
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
    signi = "low"
    avg_candle_size = abs(ohlc_df["close"] - ohlc_df["open"]).median()
    sup, res = res_sup(ohlc_df, ohlc_day)

    if (sup - 1.5 * avg_candle_size) < ohlc_df["close"][-1] < (sup + 1.5 * avg_candle_size):
        signi = "HIGH"

    if (res - 1.5 * avg_candle_size) < ohlc_df["close"][-1] < (res + 1.5 * avg_candle_size):
        signi = "HIGH"

    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df["close"][-1] > ohlc_df["close"][-2] \
            and ohlc_df["close"][-1] > ohlc_df["open"][-1]:
        pattern = "doji_bullish"

    if candle_type(ohlc_df) == 'doji' \
            and ohlc_df["close"][-1] < ohlc_df["close"][-2] \
            and ohlc_df["close"][-1] < ohlc_df["open"][-1]:
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
            and ohlc_df["high"][-1] < ohlc_df["close"][-2] \
            and ohlc_df["low"][-1] > ohlc_df["open"][-2]:
        pattern = "harami_cross_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) == "doji" \
            and ohlc_df["high"][-1] < ohlc_df["open"][-2] \
            and ohlc_df["low"][-1] > ohlc_df["close"][-2]:
        pattern = "harami_cross_bullish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "uptrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df["open"][-1] > ohlc_df["high"][-2] \
            and ohlc_df["close"][-1] < ohlc_df["low"][-2]:
        pattern = "engulfing_bearish"

    if trend(ohlc_df.iloc[:-1, :], 7) == "downtrend" \
            and candle_type(ohlc_df) != "doji" \
            and ohlc_df["close"][-1] > ohlc_df["high"][-2] \
            and ohlc_df["open"][-1] < ohlc_df["low"][-2]:
        pattern = "engulfing_bullish"

    return "Significance - {}, Pattern - {}".format(signi, pattern)


##############################################################################################
tickers = ["ZEEL", "WIPRO", "VEDL", "ULTRACEMCO", "UPL", "TITAN", "TECHM", "TATASTEEL",
           "TATAMOTORS", "TCS", "SUNPHARMA", "SBIN", "SHREECEM", "RELIANCE", "POWERGRID",
           "ONGC", "NESTLEIND", "NTPC", "MARUTI", "M&M", "LT", "KOTAKBANK", "JSWSTEEL", "INFY",
           "INDUSINDBK", "IOC", "ITC", "ICICIBANK", "HDFC", "HINDUNILVR", "HINDALCO",
           "HEROMOTOCO", "HDFCBANK", "HCLTECH", "GRASIM", "GAIL", "EICHERMOT", "DRREDDY",
           "COALINDIA", "CIPLA", "BRITANNIA", "INFRATEL", "BHARTIARTL", "BPCL", "BAJAJFINSV",
           "BAJFINANCE", "BAJAJ-AUTO", "AXISBANK", "ASIANPAINT", "ADANIPORTS", "IDEA",
           "MCDOWELL-N", "UBL", "NIACL", "SIEMENS", "SRTRANSFIN", "SBILIFE", "PNB",
           "PGHH", "PFC", "PEL", "PIDILITIND", "PETRONET", "PAGEIND", "OFSS", "NMDC", "NHPC",
           "MOTHERSUMI", "MARICO", "LUPIN", "L&TFH", "INDIGO", "IBULHSGFIN", "ICICIPRULI",
           "ICICIGI", "HINDZINC", "HINDPETRO", "HAVELLS", "HDFCLIFE", "HDFCAMC", "GODREJCP",
           "GICRE", "DIVISLAB", "DABUR", "DLF", "CONCOR", "COLPAL", "CADILAHC", "BOSCHLTD",
           "BIOCON", "BERGEPAINT", "BANKBARODA", "BANDHANBNK", "BAJAJHLDNG", "DMART",
           "AUROPHARMA", "ASHOKLEY", "AMBUJACEM", "ADANITRANS", "ACC",
           "WHIRLPOOL", "WABCOINDIA", "VOLTAS", "VINATIORGA", "VBL", "VARROC", "VGUARD",
           "UNIONBANK", "UCOBANK", "TRENT", "TORNTPOWER", "TORNTPHARM", "THERMAX", "RAMCOCEM",
           "TATAPOWER", "TATACONSUM", "TVSMOTOR", "TTKPRESTIG", "SYNGENE", "SYMPHONY",
           "SUPREMEIND", "SUNDRMFAST", "SUNDARMFIN", "SUNTV", "STRTECH", "SAIL", "SOLARINDS",
           "SHRIRAMCIT", "SCHAEFFLER", "SANOFI", "SRF", "SKFINDIA", "SJVN", "RELAXO",
           "RAJESHEXPO", "RECLTD", "RBLBANK", "QUESS", "PRESTIGE", "POLYCAB", "PHOENIXLTD",
           "PFIZER", "PNBHOUSING", "PIIND", "OIL", "OBEROIRLTY", "NAM-INDIA", "NATIONALUM",
           "NLCINDIA", "NBCC", "NATCOPHARM", "MUTHOOTFIN", "MPHASIS", "MOTILALOFS", "MINDTREE",
           "MFSL", "MRPL", "MANAPPURAM", "MAHINDCIE", "M&MFIN", "MGL", "MRF", "LTI", "LICHSGFIN",
           "LTTS", "KANSAINER", "KRBL", "JUBILANT", "JUBLFOOD", "JINDALSTEL", "JSWENERGY",
           "IPCALAB", "NAUKRI", "IGL", "IOB", "INDHOTEL", "INDIANB", "IBVENTURES", "IDFCFIRSTB",
           "IDBI", "ISEC", "HUDCO", "HONAUT", "HAL", "HEXAWARE", "HATSUN", "HEG", "GSPL",
           "GUJGASLTD", "GRAPHITE", "GODREJPROP", "GODREJIND", "GODREJAGRO", "GLENMARK",
           "GLAXO", "GILLETTE", "GMRINFRA", "FRETAIL", "FCONSUMER", "FORTIS", "FEDERALBNK",
           "EXIDEIND", "ESCORTS", "ERIS", "ENGINERSIN", "ENDURANCE", "EMAMILTD", "EDELWEISS",
           "EIHOTEL", "LALPATHLAB", "DALBHARAT", "CUMMINSIND", "CROMPTON", "COROMANDEL", "CUB",
           "CHOLAFIN", "CHOLAHLDNG", "CENTRALBK", "CASTROLIND", "CANBK", "CRISIL", "CESC",
           "BBTC", "BLUEDART", "BHEL", "BHARATFORG", "BEL", "BAYERCROP", "BATAINDIA",
           "BANKINDIA", "BALKRISIND", "ATUL", "ASTRAL", "APOLLOTYRE", "APOLLOHOSP",
           "AMARAJABAT", "ALKEM", "APLLTD", "AJANTPHARM", "ABFRL", "ABCAPITAL", "ADANIPOWER",
           "ADANIGREEN", "ADANIGAS", "ABBOTINDIA", "AAVAS", "AARTIIND", "AUBANK", "AIAENG", "3MINDIA"]


def main():
    for ticker in tickers:
        try:
            ohlc = fetchOHLC(ticker, '5minute', 5)
            ohlc_day = fetchOHLC(ticker, 'day', 30)
            ohlc_day = ohlc_day.iloc[:-1, :]
            cp = candle_pattern(ohlc, ohlc_day)
            print(ticker, ": ", cp)
        except Exception as ex:
            print("skipping for ", ticker, f"\n{ex}")


# Continuous execution
start_time = time.time()
timeout = time.time() + 60 * 60 * 1  # 60 seconds times 60 meaning the script will run for 1 hr
while time.time() <= timeout:
    try:
        print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        time.sleep(300 - ((time.time() - start_time) % 300.0))  # 300 second interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
