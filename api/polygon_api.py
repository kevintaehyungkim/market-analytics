# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta
import multiprocessing as mp
import json
# import requests
import grequests

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







# date_start = date.today()
# dates_arr = [date_start.isoformat()]

# for i in range(0,1800): 
# 	date_past = date_start - timedelta(days = 1)
# 	dates_arr.append(date_past.isoformat())
# 	date_start = date_past
# 	# date_start = date_past


# with open('dates.json', 'w', encoding='utf-8') as f:
#     json.dump(dates_arr, f, ensure_ascii=False, indent=4)


# print(len(dates_arr))








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

tickers = ['SPY', 'DIA', 'IYT', 'VXX', 'UUP', 'JNK', 'IEF', 'TLT', 'OILK', 'GLD']
# DIA - dow jones
# IYT - transports
# IEF - us10y
# UUP - USD


# for ticker in tickers:


def fetch_ticker_data(ticker):

	history_daily = {}
	history_macd = {}
	history_20ema = {}
	history_50ema = {}
	history_100ema = {}
	history_rsi = {}

	error_dates = []

	for date in dates_arr:
		try:
		
		# data_daily = getDailyTickerData(ticker, date)
		# data_macd = getTickerMACDData(ticker, date)

			print('[' + ticker + '] ' + date)

			req_headers = {'accept': 'application/json'}
			ticker_date_urls = [
				# BASE_URL + ticker + "/" + date + "?adjusted=true&apiKey=" + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
			]
			# print(ticker_date_urls)



			requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
			results = grequests.map(requests)

			# history_daily[date] = results[0].json()
			# history_20ema[date] = results[1].json()['results']['values'][0]
			# history_50ema[date] = results[2].json()['results']['values'][0]
			# history_100ema[date] = results[3].json()['results']['values'][0]
			# history_macd[date] = results[4].json()['results']['values'][0]
			history_rsi[date] = results[0].json()['results']['values'][0]


		except:
			print('[' + ticker + '] bad date: ' + date + '---' + str(results))
			error_dates.append(date)
			continue

	while len(error_dates) > 0: 
		print('num errors for ' + ticker + ': ' + str(len(error_dates)))

		error_date = error_dates.pop()

		try:
		
		# data_daily = getDailyTickerData(ticker, date)
		# data_macd = getTickerMACDData(ticker, date)

			print('[' + ticker + '] ' + error_date)

			req_headers = {'accept': 'application/json'}
			ticker_date_urls = [
				# BASE_URL + ticker + "/" + error_date + "?adjusted=true&apiKey=" + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=20&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=50&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/ema/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=100&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				# 'https://api.polygon.io/v1/indicators/macd/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&expand_underlying=false' + '&apiKey=' + API_KEY,
				'https://api.polygon.io/v1/indicators/rsi/' + ticker + '?' + 'timestamp=' + error_date + '&timespan=day&adjusted=true&window=14&series_type=close&order=desc' + '&apiKey=' + API_KEY
			]
			# print(ticker_date_urls)



			requests = [grequests.get(u, headers=req_headers) for u in ticker_date_urls]
			results = grequests.map(requests)

			# history_daily[error_date] = results[0].json()
			# history_20ema[error_date] = results[1].json()['results']['values'][0]
			# history_50ema[error_date] = results[2].json()['results']['values'][0]
			# history_100ema[error_date] = results[3].json()['results']['values'][0]
			# data_ema_200 = getTickerEMAData(ticker, date, '200')
			# history_macd[error_date] = results[4].json()['results']['values'][0]
			history_rsi[error_date] = results[5].json()['results']['values'][0]


		except:
			print('AGAIN! [' + ticker + '] bad date: ' + error_date + '---' + str(results))
			error_dates.append(date)
			continue


	with open('raw/' + ticker + '_daily_data.json', 'w', encoding='utf-8') as f:
	    json.dump(history_daily, f, ensure_ascii=False, indent=4)

	with open('raw/' + ticker + '_macd_data.json', 'w', encoding='utf-8') as f:
	    json.dump(history_macd, f, ensure_ascii=False, indent=4)

	with open('raw/' + ticker + '_20ema_data.json', 'w', encoding='utf-8') as f:
		json.dump(history_20ema, f, ensure_ascii=False, indent=4)

	with open('raw/' + ticker + '_50ema_data.json', 'w', encoding='utf-8') as f:
		json.dump(history_50ema, f, ensure_ascii=False, indent=4)

	with open('raw/' + ticker + '_100ema_data.json', 'w', encoding='utf-8') as f:
		json.dump(history_100ema, f, ensure_ascii=False, indent=4)

	with open('raw/' + ticker + '_rsi_data.json', 'w', encoding='utf-8') as f:
	    json.dump(history_rsi, f, ensure_ascii=False, indent=4)



	print (ticker + 'daily: ' + str(len(history_daily.keys())))
	print (ticker + 'macd: ' + str(len(history_macd.keys())))
	print (ticker + '20ema: ' + str(len(history_20ema.keys())))
	print (ticker + '50ema: ' + str(len(history_50ema.keys())))
	print (ticker + '100ema: ' + str(len(history_100ema.keys())))
	print (ticker + 'rsi: ' + str(len(history_rsi.keys())))


		
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




pool = mp.Pool(len(tickers)*6*20)
geocode_data = pool.map(fetch_ticker_data,tickers)

pool.close()
pool.join()





