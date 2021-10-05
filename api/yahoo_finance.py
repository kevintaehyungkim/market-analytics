import requests
import sys
import time
import json

import api.api_utils as api_utils


API_KEY_1="DtlhadqMLT3QwPr3xiDND3CqlVO8fR8G9CvR3c2j"
API_KEY_2="4EM8PpTyLI4tn5a8tV0FJ9ibWDOobi2E9UQ2O4C0"
API_KEY_3="XZHiaPkyah38SHu5SQ5zP2Nf0SdUYGiBaktnQQbj"

API_KEYS = [API_KEY_1, API_KEY_2, API_KEY_3]
API_KEY_STRING = 'X-API-KEY'


OPTIONS_BASE_URL="https://yfapi.net/v7/finance/options/"


'''
Get stock symbol information
'''
def get_stock_data(symbol):
	return


'''
Get option chain information for stock symbol and expiry day limit

Returns:
- current price (float)
- contract expiry timestamps up to the day limit (array)
'''
def get_option_data(symbol, exp_limit_days=90): 
	req_url = OPTIONS_BASE_URL + symbol
	req_headers = {'accept': 'application/json', API_KEY_STRING: API_KEY_3}

	res = requests.get(req_url, headers=req_headers)
	data = res.json()["optionChain"]["result"][0]
	quote = data['quote']

	exp_dates = filter_expiry_timestamps(data["expirationDates"], exp_limit_days)

	ask_size, bid_size = quote['askSize'], quote['bidSize']
	curr_price = (quote['ask']*ask_size + quote['bid']*bid_size)/(ask_size+bid_size)

	return curr_price, exp_dates

'''
Get option chain for stock symbol and expiry date timestamp
'''
def get_option_chain(symbol, exp_date=None): 
	req_url = OPTIONS_BASE_URL + symbol
	req_headers = {'accept': 'application/json', API_KEY_STRING: API_KEY_3}

	if exp_date:
		req_url += '?date=' + str(exp_date)

	res = requests.get(req_url, headers=req_headers)
	data = res.json()["optionChain"]["result"][0]

	option_chain = data['options'][0]
	call_chain, put_chain = option_chain['calls'], option_chain['puts']

	return call_chain, put_chain



'''
Get option chain information for stock symbol and expiry day limit

Returns:
- current price (float)
- contract expiry timestamps up to the day limit (array)
'''
def find_expiry_timestamps(symbol, exp_limit_days=90): 
	req_url = OPTIONS_BASE_URL + symbol
	req_headers = {'accept': 'application/json', API_KEY_STRING: API_KEY_3}

	res = requests.get(req_url, headers=req_headers)
	data = res.json()["optionChain"]["result"][0]
	quote = data['quote']

	exp_dates = filter_expiry_timestamps(data["expirationDates"], exp_limit_days)

	return exp_dates



'''
Filter expiry dates for number of days into the future - defaults to 90 days
'''
def filter_expiry_timestamps(expiry_timestamps, days):
	curr_timestamp = int(time.time())
	filter_timestamp = curr_timestamp + days*86400

	return [exp for exp in expiry_timestamps if exp <= filter_timestamp]














'''
#jim simmons
#price, volume, volatility

spy, qqq 
- large market-cap
- daily candles only 

1. one of the variables
price - high, mid, low (channels, moving averages)
volume - high, mid, low
volatility - high, mid, low

2^3 = 8 sections


2. options volume/oi on strikes


3. dollar index(dxy), yields(us10y), junk bonds



- unusual large amount otm - not hedging?


- 1 strategy = 1 set of outcomes that will be optimal
- multiple strategies = series of strategies -> more 

higher gamma - buy more shares to stay hedged

'''