# -*- coding: utf-8 -*-

import multiprocessing as mp
import json
import requests
import grequests

from collections import OrderedDict
from datetime import date
from datetime import timedelta


# 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(d, "day", "month")
# https://api.polygon.io/v1/open-close/AAPL/2023-05-03?adjusted=true&apiKey=xIvCOg6H8GOJNjouaTPpZ6xryChepEvt
API_KEY = 'xIvCOg6H8GOJNjouaTPpZ6xryChepEvt'
BASE_URL = "https://api.polygon.io/v1/open-close/"

def getDailyTickerData(ticker, date):
	req_url = BASE_URL + ticker + '/' + date + '?adjusted=true&apiKey=' + API_KEY
	req_headers = {'accept': 'application/json'}

	res = requests.get(req_url, headers=req_headers)
	data = res.json()
	
	return data

def getTickerEMAData(ticker, date, period):
	# https://api.polygon.io/v1/indicators/ema/AAPL?timespan=day&adjusted=true&window=50&series_type=close&order=desc&apiKey=xIvCOg6H8GOJNjouaTPpZ6xryChepEvt
	req_url = 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date 
	req_url += '&timespan=day&adjusted=true&window=' + period + '&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY
	
	req_headers = {'accept': 'application/json'}

	res = requests.get(req_url, headers=req_headers)
	data = res.json()['results']['values'][0]
	
	return data

def getTickerMACDData(ticker, date):
	# https://api.polygon.io/v1/indicators/macd/AAPL?timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey=xIvCOg6H8GOJNjouaTPpZ6xryChepEvt
	
	req_url = 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + date 
	req_url += '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=true&order=desc' + '&apiKey=' + API_KEY
	req_headers = {'accept': 'application/json'}

	res = requests.get(req_url, headers=req_headers)
	data = res.json()['results']['values'][0]

	return data

def getTickerRSIData(ticker, date):
	# https://api.polygon.io/v1/indicators/rsi/AAPL?timespan=day&adjusted=true&window=14&series_type=close&order=desc&apiKey=xIvCOg6H8GOJNjouaTPpZ6xryChepEvt
	req_url = 'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + date 
	req_url += '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close' + '&apiKey=' + API_KEY
	req_headers = {'accept': 'application/json'}
	
	res = requests.get(req_url, headers=req_headers)
	data = res.json()['results']['values'][0]
	
	return data





history_daily = {}
history_macd = {}
history_20ema = {}
history_50ema = {}
history_100ema = {}
history_200ema = {}
history_rsi = {}

f = open('stock_dates.json')
dates_arr = json.load(f)
dates_arr= dates_arr[:850]
# stock_dates = []

# tickers = ['SPY', 'DIA', 'IYT', 'VXX', 'UUP', 'JNK', 'IEF', 'TLT', 'OILK', 'GLD']
# # DIA - dow jones
# # IYT - transports
# # IEF - us10y
# # UUP - USD


# # for ticker in tickers:


# def fetch_ticker_data(ticker):

# 	history_daily = {}
# 	history_macd = {}
# 	history_20ema = {}
# 	history_50ema = {}
# 	history_100ema = {}
# 	history_rsi = {}

# 	error_dates = []

# 	for date in dates_arr:
# 		try:
		
# 		# data_daily = getDailyTickerData(ticker, date)
# 		# data_macd = getTickerMACDData(ticker, date)

# 			print('[' + ticker + '] ' + date)

# 			req_headers = {'accept': 'application/json'}
# 			ticker_date_urls = [
# 				# BASE_URL + ticker + "/" + date + "?adjusted=true&apiKey=" + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
# 			]
# 			# print(ticker_date_urls)



# 			requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
# 			results = grequests.map(requests)

# 			# history_daily[date] = results[0].json()
# 			# history_20ema[date] = results[1].json()['results']['values'][0]
# 			# history_50ema[date] = results[2].json()['results']['values'][0]
# 			# history_100ema[date] = results[3].json()['results']['values'][0]
# 			# history_macd[date] = results[4].json()['results']['values'][0]
# 			history_rsi[date] = results[0].json()['results']['values'][0]


# 		except:
# 			print('[' + ticker + '] bad date: ' + date + '---' + str(results))
# 			error_dates.append(date)
# 			continue

# 	while len(error_dates) > 0: 
# 		print('num errors for ' + ticker + ': ' + str(len(error_dates)))

# 		error_date = error_dates.pop()

# 		try:
		
# 		# data_daily = getDailyTickerData(ticker, date)
# 		# data_macd = getTickerMACDData(ticker, date)

# 			print('[' + ticker + '] ' + error_date)

# 			req_headers = {'accept': 'application/json'}
# 			ticker_date_urls = [
# 				# BASE_URL + ticker + "/" + error_date + "?adjusted=true&apiKey=" + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
# 				'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
# 			]
# 			# print(ticker_date_urls)



# 			requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
# 			results = grequests.map(requests)

# 			# history_daily[error_date] = results[0].json()
# 			# history_20ema[error_date] = results[1].json()['results']['values'][0]
# 			# history_50ema[error_date] = results[2].json()['results']['values'][0]
# 			# history_100ema[error_date] = results[3].json()['results']['values'][0]
# 			# data_ema_200 = getTickerEMAData(ticker, date, '200')
# 			# history_macd[error_date] = results[4].json()['results']['values'][0]
# 			history_rsi[error_date] = results[5].json()['results']['values'][0]


# 		except:
# 			print('AGAIN! [' + ticker + '] bad date: ' + error_date + '---' + str(results))
# 			error_dates.append(date)
# 			continue


# 	print (ticker + 'daily: ' + str(len(history_daily.keys())))
# 	print (ticker + 'macd: ' + str(len(history_macd.keys())))
# 	print (ticker + '20ema: ' + str(len(history_20ema.keys())))
# 	print (ticker + '50ema: ' + str(len(history_50ema.keys())))
# 	print (ticker + '100ema: ' + str(len(history_100ema.keys())))
# 	print (ticker + 'rsi: ' + str(len(history_rsi.keys())))


		
		# data_daily = getDailyTickerData(ticker, date)
		# data_macd = getTickerMACDData(ticker, date)
		# data_ema_20 = getTickerEMAData(ticker, date, '20')
		# data_ema_50 = getTickerEMAData(ticker, date, '50')
		# data_ema_100 = getTickerEMAData(ticker, date, '100')
		# # data_ema_200 = getTickerEMAData(ticker, date, '200')
		# data_rsi = getTickerRSIData(ticker, date)
		
		# history_daily[date]=data_daily
		# history_macd[date]=data_macd
		# history_20ema[date]=data_ema_20
		# history_50ema[date]=data_ema_50
		# history_100ema[date]=data_ema_100
		# history_200ema[date]=data_ema_200
		# history_rsi[date]=data_rsi
		
		# stock_dates.append(date)
	



# for ticker in tickers: 
# 	for 

# LINES = []
# k=time.time()
# line_urls = ["http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=1&key=MW9S-E7SL-26DU-VV8V&json=y",
# 				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=3&key=MW9S-E7SL-26DU-VV8V&json=y",
# 				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=5&key=MW9S-E7SL-26DU-VV8V&json=y",
# 				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=7&key=MW9S-E7SL-26DU-VV8V&json=y",
# 				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=11&key=MW9S-E7SL-26DU-VV8V&json=y"]
# responses = [grequests.get(u) for u in line_urls]

# for r in grequests.map(responses):
# 	LINES.append(list(r.json()["root"]["routes"]["route"]["config"]["station"]))

# q = time.time()
# print(q-k)

	# with open('stock_dates.json', 'w', encoding='utf-8') as f:
	#     json.dump(stock_dates, f, ensure_ascii=False, indent=4)



timestamps = []

def fetch_hourly_data():

	history_hourly = {}
	history_macd = {}
	history_rsi = {}

	total = []

	error_dates = []

	next_urls = ["https://api.polygon.io/v2/aggs/ticker/SPY/range/1/hour/2018-05-30/2023-05-09?adjusted=true&sort=asc&limit=50000&apiKey=" + API_KEY]

	while len(next_urls) > 0:

		req_headers = {'accept': 'application/json'}
		next_url = next_urls.pop()

		res = requests.get(next_url, headers=req_headers)
		data = res.json()

		total.extend(data['results'])

		try:
			if data['next_url']:
				print(data['next_url'])
				next_urls.append(data['next_url']+"&apiKey=" + API_KEY)
		except: 
			break

	print("timestamps total: " + str(len(total)))

	for t in total:
		timestamps.append(t['t'])

	return total



def fetch_rsi_data(t):
	print(t)
	req_headers = {'accept': 'application/json'}
	url = "https://api.polygon.io/v1/indicators/rsi/SPY?timestamp=" + str(t) + "&timespan=hour&adjusted=true&window=14&series_type=close&order=asc&apiKey=" + API_KEY
	res = requests.get(url, headers=req_headers)
	data = res.json()

	return {'t': t, 'c': data['results']['values'][0]['value']}

def fetch_macd_data(t):
	print(t)
	req_headers = {'accept': 'application/json'}
	url = "https://api.polygon.io/v1/indicators/macd/SPY?timestamp=" + str(t) + "&timespan=hour&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey=" + API_KEY
	res = requests.get(url, headers=req_headers)
	data = res.json()['results']['values'][0]

	return data


	# for date in dates_arr:
	# 	try:
		
	# 	# data_daily = getDailyTickerData(ticker, date)
	# 	# data_macd = getTickerMACDData(ticker, date)

	# 		print('[' + ticker + '] ' + date)

	# 		req_headers = {'accept': 'application/json'}
	# 		ticker_date_urls = [
	# 			# BASE_URL + ticker + "/" + date + "?adjusted=true&apiKey=" + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
	# 		]
	# 		# print(ticker_date_urls)



	# 		requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
	# 		results = grequests.map(requests)

	# 		# history_daily[date] = results[0].json()
	# 		# history_20ema[date] = results[1].json()['results']['values'][0]
	# 		# history_50ema[date] = results[2].json()['results']['values'][0]
	# 		# history_100ema[date] = results[3].json()['results']['values'][0]
	# 		# history_macd[date] = results[4].json()['results']['values'][0]
	# 		history_rsi[date] = results[0].json()['results']['values'][0]


	# 	except:
	# 		print('[' + ticker + '] bad date: ' + date + '---' + str(results))
	# 		error_dates.append(date)
	# 		continue

	# while len(error_dates) > 0: 
	# 	print('num errors for ' + ticker + ': ' + str(len(error_dates)))

	# 	error_date = error_dates.pop()

	# 	try:
		
	# 	# data_daily = getDailyTickerData(ticker, date)
	# 	# data_macd = getTickerMACDData(ticker, date)

	# 		print('[' + ticker + '] ' + error_date)

	# 		req_headers = {'accept': 'application/json'}
	# 		ticker_date_urls = [
	# 			# BASE_URL + ticker + "/" + error_date + "?adjusted=true&apiKey=" + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
	# 			'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
	# 		]
	# 		# print(ticker_date_urls)



	# 		requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
	# 		results = grequests.map(requests)

	# 		# history_daily[error_date] = results[0].json()
	# 		# history_20ema[error_date] = results[1].json()['results']['values'][0]
	# 		# history_50ema[error_date] = results[2].json()['results']['values'][0]
	# 		# history_100ema[error_date] = results[3].json()['results']['values'][0]
	# 		# data_ema_200 = getTickerEMAData(ticker, date, '200')
	# 		# history_macd[error_date] = results[4].json()['results']['values'][0]
	# 		history_rsi[error_date] = results[5].json()['results']['values'][0]


	# 	except:
	# 		print('AGAIN! [' + ticker + '] bad date: ' + error_date + '---' + str(results))
	# 		error_dates.append(date)
	# 		continue


	# with open('raw/SPY_hourly_data.json', 'w', encoding='utf-8') as f:
	# 	json.dump(total, f, ensure_ascii=False, indent=4)



def calculate_ema(data, days, smoothing=2):
	days = days 
	timestamps = [d['t'] for d in data][days-1:]
	prices = [d['c'] for d in data]

	ema = [sum(prices[:days]) / days]
	for price in prices[days:]:
		ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
	
	print("ema" + str(days/7) + "last val: " + str(ema[-1]))
	# print(len(timestamps))

	ema_data = OrderedDict()
	for i in range(days, len(timestamps)):
		ema_data[timestamps[i]] = ema[i]

	return ema_data


def calculate_sma(data, period):
	sma_timestamps = [d['t'] for d in data][period-1:]
	prices = [d['c'] for d in data]
	
	window_size = period
	sma = []

	i = 0
	while i < len(prices) - window_size + 1:
		window = prices[i : i + window_size]
		window_average = round(sum(window) / window_size, 2)
		sma.append(window_average)

		i += 1

	print("sma " + str(period) + "last val: " + str(sma[-1]))

	sma_data = OrderedDict()
	for j in range(len(sma_timestamps)):
		sma_data[sma_timestamps[j]] = sma[j]

	return sma_data


def calculate_macd(sma12_data, ema26_data):
	macd_arr = []
	macd_data = OrderedDict()

	for t, ema26 in ema26_data.items():
		macd = sma12_data[t] - ema26
		macd_arr.append({'t': t, 'c': macd})
	
	signal_data = calculate_ema(macd_arr, 9)

	i = 8
	for t, signal in signal_data.items():
		macd = macd_arr[i]['c']
		macd_data[t] = {
			"timestamp": t,
			"value": macd,
			"signal": signal,
			"histogram": macd-signal
		}
		i += 1

	return macd_data


def calculate_rsi(price_data):
	# RSI = 100 – (100 / [1 + {14-Day Average Gain / 14-Day Average Loss}])
	period = 14 

	gain_14d = []
	loss_14d = []
	rsi_arr = []
	rsi_data = OrderedDict()

	price_prev = price_data[0]['c']

	for price in price_data[1:period]:
		price_curr = price['c']
		diff = price['c'] - price_prev
		if diff >= 0:
			gain_14d.append(diff)
			loss_14d.append(0)
		else:
			gain_14d.append(0)
			loss_14d.append(abs(diff))
		price_prev = price_curr


	for price in price_data[period:]:

		timestamp = price['t']
		price_curr = price['c']
		avg_gain = sum(gain_14d)/period
		avg_loss = sum(loss_14d)/period

		diff = price_curr - price_prev
		if diff >= 0:
			gain_14d.append(diff)
			loss_14d.append(0)
		else:
			gain_14d.append(0)
			loss_14d.append(abs(diff))

		if avg_loss == 0:
			avg_loss = 0.01

		rsi = 100 - (100/(1+avg_gain/avg_loss))
		rsi_arr.append({'t': timestamp, 'c': rsi})

		gain_14d.pop(0)
		loss_14d.pop(0)

		price_prev = price_curr

	rsi_14sma_data = calculate_sma(rsi_arr, 14)
	i = period-1

	for t, sma in rsi_14sma_data.items():
		rsi_data[t] = {
			'rsi': rsi_arr[i]['c'], 
			'rsi_14sma': sma
		}
		i += 1

	return rsi_data


def add_rsi_sma(rsi_arr, sma_period=14):
	rsi_sma_data = calculate_sma(rsi_arr, sma_period)
	rsi_data = {}

	i = sma_period-1
	for t, sma in rsi_sma_data.items():
		rsi_data[t] = {
			'rsi': rsi_arr[i]['c'], 
			'rsi_14sma': sma
		}
		i += 1

	return rsi_data



hourly_data = fetch_hourly_data()



pool = mp.Pool(50)
rsi_ = pool.map(fetch_rsi_data,timestamps)

pool.close()
pool.join()

rsi2 = add_rsi_sma(rsi_, 14)



# pool = mp.Pool(50)
# macd_ = pool.map(fetch_macd_data, timestamps)
# pool.close()
# pool.join()

# macd2 = {}
# for m in macd_:
# 	macd2[str(m['timestamp'])] = {
# 		'value': m['value'], 
# 		'signal': m['signal'],
# 		'histogram': m['histogram']
# 	}




# with open('raw/SPY/1h/macd.json', 'w', encoding='utf-8') as f:
#     json.dump(macd2, f, ensure_ascii=False, indent=4)

with open('raw/SPY/1h/rsi.json', 'w', encoding='utf-8') as f:
	json.dump(rsi2, f, ensure_ascii=False, indent=4)

# with open('raw/SPY/1h/100ema.json', 'w', encoding='utf-8') as f:
# 	json.dump(ema100, f, ensure_ascii=False, indent=4)

# with open('raw/SPY/1h/200ema.json', 'w', encoding='utf-8') as f:
# 	json.dump(ema200, f, ensure_ascii=False, indent=4)



with open('raw/SPY/1h/timestamps.json', 'w', encoding='utf-8') as f:
	json.dump(timestamps, f, ensure_ascii=False, indent=4)

prices = {}
for h in hourly_data:
	if h['t'] >= 1530788400000:
		prices[h['t']] = {
			"open": h['o'],
	        "high": h['h'],
	        "low": h['l'],
	        "close": h['c'],
	        "vol": h['v']
		}

with open('raw/SPY/1h/prices.json', 'w', encoding='utf-8') as f:
	json.dump(prices, f, ensure_ascii=False, indent=4)


# print(len(ema100))
# print(len(ema200))

