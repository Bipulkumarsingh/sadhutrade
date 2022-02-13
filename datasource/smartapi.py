import pandas as pd
from smartapi import SmartConnect  # or from smartapi.smartConnect import SmartConnect
from smartapi.smartExceptions import *
from src.constants import get_config

smart_config = get_config('angelOne')
# create object of call
obj = SmartConnect(api_key=smart_config["apiKey"]
                   # optional
                   # access_token = "your access token",
                   # refresh_token = "your refresh_token"
                   )

# login api call
data = obj.generateSession(smart_config["userId"], smart_config["password"])
refreshToken = data['data']['refreshToken']

# fetch the feedtoken
feedToken = obj.getfeedToken()

# fetch User Profile
userProfile = obj.getProfile(refreshToken)

print(userProfile)


def historical_data(symbol_token: int, interval: str, from_date: str, to_date: str):
    """
        Returns historical data for the stock with the selected timeframe (from_date - to_date).

        Parameters:
            symbol_token: int (Ex: 3045)
            interval: str (Ex: ONE_MINUTE)
            from_date: str (Ex: 2021-10-22 09:15)
            to_date: str (Ex: 2021-10-22 15:30)

        Return:
            df: DataFrame
    """
    # Historic api
    try:
        historicParam = {
            "exchange": "NSE",
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }
        # Retrieving historical data
        records = obj.getCandleData(historicParam)['data']

        # Create the pandas DataFrame
        df = pd.DataFrame(records, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df.date)
        df['date'] = df['date'].dt.strftime('%d/%m/%Y %H:%M:%S')
        print(df)
    except InputException as ie:
        print(ie)

# #logout
# try:
#     logout=obj.terminateSession('Your Client Id')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))


# #place order
# try:
#     orderparams = {
#         "variety": "NORMAL",
#         "tradingsymbol": "SBIN-EQ",
#         "symboltoken": "3045",
#         "transactiontype": "BUY",
#         "exchange": "NSE",
#         "ordertype": "LIMIT",
#         "producttype": "INTRADAY",
#         "duration": "DAY",
#         "price": "19500",
#         "squareoff": "0",
#         "stoploss": "0",
#         "quantity": "1"
#         }
#     orderId=obj.placeOrder(orderparams)
#     print("The order id is: {}".format(orderId))
# except Exception as e:
#     print("Order placement failed: {}".format(e.message))


# #gtt rule creation
# try:
#     gttCreateParams={
#             "tradingsymbol" : "SBIN-EQ",
#             "symboltoken" : "3045",
#             "exchange" : "NSE",
#             "producttype" : "MARGIN",
#             "transactiontype" : "BUY",
#             "price" : 100000,
#             "qty" : 10,
#             "disclosedqty": 10,
#             "triggerprice" : 200000,
#             "timeperiod" : 365
#         }
#     rule_id=obj.gttCreateRule(gttCreateParams)
#     print("The GTT rule id is: {}".format(rule_id))
# except Exception as e:
#     print("GTT Rule creation failed: {}".format(e.message))


# #gtt rule list
# try:
#     status=["FORALL"] #should be a list
#     page=1
#     count=10
#     lists=obj.gttLists(status,page,count)
#     print(lists)
# except Exception as e:
#     print("GTT Rule List failed: {}".format(e.message))
