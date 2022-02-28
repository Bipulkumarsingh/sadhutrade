import falcon.asgi
from services.trade import Home

app = falcon.asgi.App()


app.add_route('/home', Home())

# import json
# from src.constants import ROOT_DIR
#
# with open(f'{ROOT_DIR}/config/instruments.json', 'r') as file:
#     instrument_dump = json.load(file)
#     temp = [(instrument['symbol'], instrument['token']) for instrument in instrument_dump
#             if instrument['exch_seg'] == 'NSE' and instrument['symbol'].endswith('-EQ')]
#
# with open(f'{ROOT_DIR}/config/config.json', 'r+') as jsonFile:
#     temp_config = json.load(jsonFile)
#     temp_config['tickers']['smartApi'] = temp
#
#     jsonFile.seek(0)  # Move the cursor back to the beginning of the file
#     json.dump(temp_config, jsonFile, indent=4, sort_keys=True)
#     jsonFile.truncate()
