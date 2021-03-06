import json
import requests


'''
key: candlestick intervals (string), 
value: # seconds (int)
'''

CANDLESTICK_INTERVALS = {
	'1H': 3600,

	# ...

	'1W': 604800
}


TIME_INTERVALS = {
	'1H': 3600,

	# ...

	'1W': 604800
}



'''
date converter
'''



'''
Filter expiry dates for number of days into the future - defaults to 90 days
'''
def make_request(url, headers, api_keys):
	for api_key in api_keys:
		try:
			res = requests.get(req_url, headers=req_headers)
			data = res.json()
			return data
		except:
			continue
	return "No API key currently available"


'''
Filter expiry dates for number of days into the future - defaults to 90 days
'''
def filter_expiry_timestamps(expiry_timestamps, days=400):
	curr_timestamp = int(time.time())
	filter_timestamp = curr_timestamp + days*86400

	return [exp for exp in expiry_timestamps if exp <= filter_timestamp]


def convert_option_date_to_timestamp():
	return


def convert_timestamp_to_option_date():
	return



