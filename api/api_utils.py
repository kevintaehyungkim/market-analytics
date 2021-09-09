 
import json
import requests
import sys


'''
Filter expiry dates for number of days into the future - defaults to 90 days
'''
def make_request(url, key_string, api_keys):
	for api_key in api_keys:
		req_headers = {'accept': 'application/json', key_string: api_key}
		try:
			res = requests.get(req_url, headers=req_headers)
			print(res)
			data = res.json()
			print(data)
			return data
		except:
			continue

	raise RuntimeError("No available API key")

