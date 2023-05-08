
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


sys.path.append('../')

import api.api_utils as api_utils
import data.data_loader as data

from collections import OrderedDict

DATA_MAP = data.DATA_MAP
MARKET_DATES = data.MARKET_DATES
MARKET_DATES.reverse()

NUM_DATES = len(MARKET_DATES)

# print(MARKET_DATES[0])
# print(MARKET_DATES[len(MARKET_DATES)-1])
# print(NUM_DATES)



def generate_output():
	output_arr = []
	i, interval = 55, 30

	while i + interval <= NUM_DATES:
		temp_dates = MARKET_DATES[i:i+interval]
		temp_data = [data.SPY_DAILY[date] for date in temp_dates]

		start = temp_data[0]
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



'''
Day K

Within the trend biggest diff we can find (how volatile and good for trading)
OUTCOME: INTERNAL SPY TREND 1 MONTH AVG MEAN (DAY K -> DAY K + 30) 
- Within the next 30 days, price is higher or lower?
- For either, find global maxima if higher and global minima if lower and return % diff from day k
- If same, return biggest diff in whichever direction it exists  

INPUTS: 
'''
FIBONACCI = [1,2,3,5,8,13,21,34,55]
CALIBRATED = {'VIX', 'US10Y'}

def generate_features():
	rows = []

	# for ticker in ['SPY']: 

	# 	ticker_arr = []

	# 	# EMA
	# 	ema20_data = DATA_MAP[ticker]['EMA20']
	# 	ema50_data = DATA_MAP[ticker]['EMA20']
	# 	ema100_data = DATA_MAP[ticker]['EMA20']

	i, interval = 0, 55

	while i + interval <= NUM_DATES - 30:

		# DAILY
		temp_dates = MARKET_DATES[i:i+interval]
		row = []
		# print(temp_dates[0] + ' - ' + temp_dates[-1])

		for ticker in data.tickers: 

			daily_data = [DATA_MAP[ticker]['DAILY'][date] for date in temp_dates]
			ema20_data = [DATA_MAP[ticker]['EMA20'][date]['value'] for date in temp_dates]
			ema50_data = [DATA_MAP[ticker]['EMA50'][date]['value'] for date in temp_dates]
			ema100_data = [DATA_MAP[ticker]['EMA100'][date]['value'] for date in temp_dates]
			macd_data = [DATA_MAP[ticker]['MACD'][date] for date in temp_dates]

			end_price = daily_data[-1]['close']

			for fib in FIBONACCI:
				k = -1*fib

				curr_price = daily_data[k]['open']
				price_change = ((end_price-curr_price)/curr_price)*100
				row.append(price_change)

				curr_ema20 = ema20_data[k]
				ema20_diff = curr_price-curr_ema20
				row.append(ema20_diff)

				curr_ema50 = ema50_data[k]
				ema50_diff = curr_price-curr_ema50
				row.append(ema50_diff)

				curr_ema100 = ema100_data[k]
				ema100_diff = curr_price-curr_ema100
				row.append(ema100_diff)

				row.append(macd_data[k]['value'])
				row.append(macd_data[k]['histogram'])

		i += 1
		rows.append(row)

	print("number of rows: " + str(len(rows)))
	print("number of columns: " + str(len(rows[0])))

	return rows


			# feature_arr.append()


output = generate_output()
features = generate_features()

for i in range(len(features)):
	features[i].append(output[i])

print("number of rows: " + str(len(features)))
print("number of columns: " + str(len(features[0])))


import csv

with open('processed/data1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = [str(i) for i in range(541)]
    
    writer.writerow(field)

    for feature in features: 
    	writer.writerow(feature)



# make sure to import all of our modules
# sklearn package
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# dataframes
import pandas as pd
# computation
import numpy as np
# visualization
import matplotlib.pyplot as plt

# dataset
# https://www.kaggle.com/datasets/ciphernine/brooklyn-real-estate-listings
# place it in the same folder as this workbook
df = pd.read_csv('processed/data1.csv')

# for this example, we're going to estimate the price with sqft, bathroom, and bedrooms
df = df[[str(i) for i in range(541)]].dropna()

# show some random lines from our data
print(df.sample(n=15))

x_values = df[[str(i) for i in range(540)]].values
y_values = df['540'].values

degree = 2
poly_model = PolynomialFeatures(degree=2)
poly_x_values = poly_model.fit_transform(x_values)

print ("initial values mapped")

poly_model.fit(poly_x_values, y_values)

regression_model = LinearRegression()
regression_model.fit(poly_x_values, y_values)

y_pred = regression_model.predict(poly_x_values)

regression_model.coef_


mean_squared_error(y_values, y_pred, squared=False)

num_degrees = [1,2,3,4,5,6,7]
plt_mean_squared_error = []



for degree in num_degrees:

   poly_model = PolynomialFeatures(degree=degree)
  
   poly_x_values = poly_model.fit_transform(x_values)
   poly_model.fit(poly_x_values, y_values)
  
   regression_model = LinearRegression()
   regression_model.fit(poly_x_values, y_values)
   y_pred = regression_model.predict(poly_x_values)

   plt_mean_squared_error.append(mean_squared_error(y_values, y_pred, squared=False))
  
plt.scatter(number_degrees,plt_mean_squared_error, color="green")
plt.plot(number_degrees,plt_mean_squared_error, color="red") 

'''
VIX
- PRICE CLOSE @ DAY k-1
- PRICE CLOSE @ DAY k-2
- PRICE CLOSE @ DAY k-3
- PRICE CLOSE @ DAY k-5
- PRICE CLOSE @ DAY k-8
- ST. DEV EMA 20 PRICE DIFF
- EMA 50 PRICE DIFF

SPY + VIX + DJT + DJI + DXY + JNK + US10Y + USOIL + GOLD
- CHANGE FROM DAY k-1 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k
- CHANGE FROM DAY k-2 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD Short Window @ Day k-1
	- MACD Short Window @ Day k-1
	- MACD Short Window @ Day k-1
	- MACD Short Window @ Day k-1
	- MACD Short Window @ Day k-1


- CHANGE FROM DAY k-3 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k

- CHANGE FROM DAY k-5 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k

- CHANGE FROM DAY k-8 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k



- CHANGE FROM DAY k-13 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k
- CHANGE FROM DAY k-21 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF
	- MACD % CHANGE FROM DAY k-1 to DAY k
- CHANGE FROM DAY k-28 to DAY k
	- ST. DEV EMA 20 PRICE DIFF
	- ST. DEV EMA 50 PRICE DIFF 
	- MACD % CHANGE FROM DAY k-1 to DAY k

DXY

USOIL 


GOLD PRICE 


SPY MACD 




'''