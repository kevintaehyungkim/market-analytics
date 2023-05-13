# -*- coding: utf-8 -*-

import sys

import api.api_utils as api_utils
import data.data_loader as data

from collections import OrderedDict

DATA_MAP = data.DATA_MAP
MARKET_DATES = data.MARKET_DATES
MARKET_DATES.reverse()


'''
- macd cross earlier then check 1 timestamp below

1. MACD + EMA 100 
2. MACD + EMA 100 + RSI mid
'''

# DEFAULT VALUES
RSI_MID = 50

MARKET_DATES = data.MARKET_DATES
MARKET_DATES.reverse()

# CUSTOM VALUES
TRADE_WINDOW = 10 #days
MIN_PROFIT = 5 #percent
TICKER_DATA = data.SPY_DAILY #ticker_timeframe




price_arr = []

def strategy_1():
	output_arr = []
	i, interval = 0, 10

	while i < NUM_DATES - interval:
		temp_dates = MARKET_DATES[i:i+interval]
		temp_data = [data.SPY_DAILY[date] for date in temp_dates]

		start = temp_data[0]
		price_arr.append(start['close'])
		end = temp_data[len(temp_data)-1]

		start_price = start['open']
		local_min = find_minima(start_price, temp_data)
		local_max = find_maxima(start_price, temp_data)
		if abs(local_min) > abs(local_max):
			output_arr.append(local_min)
		else:
			output_arr.append(local_max)

		i += 1

	print(len(output_arr))

	return output_arr
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

def find_minima(start_price, data):
	curr_min = start_price 

	for d in data:
		curr_min = min(curr_min, d['low'])

	return ((curr_min-start_price) / start_price)*100



def find_maxima(start_price, data):
	curr_max = start_price 
	
	for d in data:
		curr_max = max(curr_max, d['high'])

	return ((curr_max-start_price) / start_price)*100

