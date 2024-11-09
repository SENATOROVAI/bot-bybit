# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import requests
import config
url = "https://api-testnet.bybit.com/v5/asset/deposit/query-record"

# %%
payload={}
headers = {
  'X-BAPI-API-KEY': config.api_key,
  'X-BAPI-TIMESTAMP': '1731109354409',
  'X-BAPI-RECV-WINDOW': '20000',
  'X-BAPI-SIGN': '3846ac24f96f7a8105b165077acb50c0b95693327848c2af61b0f196d09eb9ae'
}

# %% [markdown]
# response = requests.request("GET", url, headers=headers, data=payload)

# %%
# print(response.text)
import config
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

# %%
# API keys
API_KEY = config.api_key
API_SECRET = config.api_secret

# %%
# Base URLs
BYBIT_BASE_URL = 'https://api.bybit.com'

# %%
# Constants
SYMBOL = 'BTCUSDT'
ORDER_TYPE = 'Market'
FIXED_ORDER_QTY_BTC = 0.001
QUANTITY_STEP_SIZE = 0.001

# %%
def generate_signature(secret, params):
    query_string = urlencode(sorted(params.items()))
    hmac_sha256 = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
    return hmac_sha256.hexdigest()


# %%
def get_balance(coin):
    timestamp = int(time.time() * 1000)
    params = {
        'api_key': API_KEY,
        'timestamp': timestamp,
        'coin': coin
    }
    params['sign'] = generate_signature(API_SECRET, params)
    url = f"{BYBIT_BASE_URL}/v2/private/wallet/balance"
    response = requests.get(url, params=params)
    return response
    # return response.json()
get_balance("usdt")    

# %%
from pybit.unified_trading import HTTP

API_KEY = config.api_key
API_SECRET = config.api_secret

req_timestamp = int(time.time() * 1000)

# Adjust recv_window if needed (increase by 5 or 10 seconds)
recv_window = 10000  # 10 seconds

# Example API request with the adjusted parameters
params = {
    "api_key": API_KEY,
    "req_timestamp": req_timestamp,
    "recv_window": recv_window,
    # Add other parameters here
}
# print(session.get_wallet_balance(
#     accountType="UNIFIED",
#     coin="USDT",
# ))
response = requests.get("https://api.bybit.com/v5/your_endpoint", params=params)

print(response.json())

# %%
import requests
import time
import hashlib
import hmac
import uuid

api_key=API_KEY
secret_key=API_SECRET
httpClient=requests.Session()
recv_window=str(5000)
url="https://api.bybit.com" # Testnet endpoint

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    print(response.text)
    print(response.headers)
    print(Info + " Elapsed Time : " + str(response.elapsed))

def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

# #Create Order
endpoint="/v5/market/funding/history"
# method="POST"
# orderLinkId=uuid.uuid4().hex
params=''
HTTP_Request(endpoint,method,params,"")

# #Get unfilled Orders
# endpoint="/v5/order/realtime"
# method="GET"
# params='category=linear&settleCoin=USDT'
# HTTP_Request(endpoint,method,params,"UnFilled")

# #Cancel Order
# endpoint="/v5/order/cancel"
# method="POST"
# params='{"category":"linear","symbol": "BTCUSDT","orderLinkId": "'+orderLinkId+'"}'
# HTTP_Request(endpoint,method,params,"Cancel")

# %%
from pybit.unified_trading import HTTP
session = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET
)
print(session.get_deposit_records(
    coin="USDT",
))
