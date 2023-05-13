

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


price_arr = []

def generate_output():
	output_arr = []
	i, interval = 1, 14

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

	i = 0

	while i < NUM_DATES- 14 - 1:
		row = []

		for ticker in data.tickers: 
			date = MARKET_DATES[i]

			daily_data = DATA_MAP[ticker]['DAILY']
			macd_data = DATA_MAP[ticker]['MACD']

			# print(daily_data[date])
			# print(macd_data[date])

			# row.append(daily_data[date]['close'])
			row.append(macd_data[date]['value'])
			row.append(macd_data[date]['histogram'])

	# while i + interval <= NUM_DATES - 14:

	# 	# DAILY
	# 	temp_dates = MARKET_DATES[i:i+interval]
	# 	row = []
	# 	# print(temp_dates[0] + ' - ' + temp_dates[-1])

	# 	for ticker in data.tickers: 

	# 		daily_data = [DATA_MAP[ticker]['DAILY'][date] for date in temp_dates]
	# 		ema20_data = [DATA_MAP[ticker]['EMA20'][date]['value'] for date in temp_dates]
	# 		ema50_data = [DATA_MAP[ticker]['EMA50'][date]['value'] for date in temp_dates]
	# 		ema100_data = [DATA_MAP[ticker]['EMA100'][date]['value'] for date in temp_dates]
	# 		macd_data = [DATA_MAP[ticker]['MACD'][date] for date in temp_dates]

	# 		end_price = daily_data[-1]['close']

	# 		for fib in FIBONACCI:
	# 			k = -1*fib


				# row.append(end_price)
				# curr_price = daily_data[k]['open']
				# price_change = ((end_price-curr_price)/curr_price)*100
				# row.append(price_change)

				# curr_ema20 = ema20_data[k]
				# ema20_diff = curr_price-curr_ema20
				# row.append(ema20_diff)

				# curr_ema50 = ema50_data[k]
				# ema50_diff = curr_price-curr_ema50
				# row.append(ema50_diff)

				# curr_ema100 = ema100_data[k]
				# ema100_diff = curr_price-curr_ema100
				# row.append(ema100_diff)

				# row.append(macd_data[k]['value'])
				# row.append(macd_data[k]['histogram'])

		i += 1
		rows.append(row)

	return rows


			# feature_arr.append()


output = generate_output()
print("output number of rows: " + str(len(output)))

features = generate_features()
print("features number of rows: " + str(len(features)))
print("features number of columns: " + str(len(features[0])))

for i in range(len(features)):
	features[i].append(output[i])

for i in range(len(features)):
	features[i].append(price_arr[i])

print("number of rows: " + str(len(features)))
print("number of columns: " + str(len(features[0])))



# # dataframes
import pandas as pd
# # computation
import numpy as np
# # visualization
import matplotlib.pyplot as plt
import csv

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

with open('processed/data1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = [str(i) for i in range(31)]
    
    writer.writerow(field)
    for feature in features: 
    	writer.writerow(feature)


df = pd.read_csv('processed/data1.csv')

# for this example, we're going to estimate the price with sqft, bathroom, and bedrooms
# df = df[[str(i) for i in range(541)]].dropna()

price = df['21']

x = df[[str(i) for i in range(8)]].values
y = df['20']


# x_test = x_values[-200:]
# y_test = y_values[-200:]

# x_values = x_values[:635]
# y_values = y_values[:635]
# plt.plot(np.array(range(0,835)), df['0'], color="blue")
# plt.plot(np.array(range(0,835)), df['1'], color="orange")
# plt.plot(np.array(range(0,835)), y_values, color="red")
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score#,metrics.explained_variance_score
import sklearn.linear_model as skl
import scipy.linalg as scl
from sklearn.pipeline import Pipeline
from sklearn import model_selection

err = []
bi=[]
vari=[]

n = 1000
n_boostraps = 1000

#Polynomial degree
degrees = np.arange(1,16)


#Bootstrap part
for degree in degrees:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression(fit_intercept=False))
    y_pred = np.empty((y_test.shape[0], n_boostraps))
    for i in range(n_boostraps):
        x_, y_ = resample(x_train, y_train)
        # Evaluate the new model on the same test data each time.
        y_pred[:, i] = model.fit(x_, y_).predict(x_test).ravel()
    error = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
    bias = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
    variance = np.mean( np.var(y_pred, axis=1, keepdims=True) )
    err.append(error)
    bi.append(bias)
    vari.append(variance)

max_pd = 12 #max polynomial degree to plot to
plt.figure()
plt.plot(degrees[:max_pd],err[:max_pd],'k',label='MSE')
plt.plot(degrees[:max_pd],bi[:max_pd],'b',label='Bias^2')
plt.plot(degrees[:max_pd],vari[:max_pd],'y',label='Var')
summ=np.zeros(len(vari))
for i in range(len(err)):
    summ[i]=vari[i]+bi[i]
plt.plot(degrees[:max_pd],summ[:max_pd],'ro',label='sum')

plt.xlabel('Polynomial degree')
plt.ylabel('MSE Bootstrap')
plt.legend()
plt.show()



# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm

# plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

# n = len(x_test)  # Number of samples in data
 
# iter = 0  # Initial iteration counter
# itersteps = 250  # Total number of iterations
 
# # Initial guesses for linear regression model of y=mx+b and arrays to keep track of values over iterations
# m = np.zeros(itersteps)
# b = np.zeros(itersteps)
# J = np.zeros(itersteps)
# dJdm = np.zeros(itersteps)
# dJdb = np.zeros(itersteps)
# SSR = np.zeros(itersteps)
# SSE = np.zeros(itersteps)
# SSTO = np.zeros(itersteps)
# R_sq = np.zeros(itersteps)
 
# a = 1E-5  # Step size
 
# # Gradient Descent implementation on the linear regression model
# while iter < itersteps - 1:
#     print('Iteration: ', iter)
#     y_new = m[iter] * x_test + b[iter]
 
#     J[iter] = 1 / n * np.sum((y_test - y_new) ** 2)  # Mean Squared Error
 
#     dJdm[iter] = 1 / n * np.sum((y_test - y_new) * -2 * x_test)
#     dJdb[iter] = 1 / n * np.sum((y_test - y_new) * -2)
 
#     SSR[iter] = np.sum((y_new - np.mean(y_test)) ** 2)
#     SSE[iter] = np.sum((y_test - y_new) ** 2)
#     SSTO[iter] = np.sum((y_test - np.mean(y_test)) ** 2)
#     R_sq[iter] = 1-SSE[iter]/SSTO[iter]
 
#     m[iter + 1] = m[iter] - a * dJdm[iter]
#     b[iter + 1] = b[iter] - a * dJdb[iter]
#     iter += 1
 
# # Data to create a smooth line for the linear regression model
# x_min = min(x_test)
# x_max = max(x_test)
# x = np.linspace(x_min, x_max, n)
# y = m[0] * x + b[0]
 
# # Creating initial figure
# fig1, ax, = plt.subplots(figsize=(10, 10))
# ax.scatter(x_test, y_test)  # Initial scatter plot that does not get updated
# line, = ax.plot(x, y, 'red')  # Initial linear fit
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# t1 = ax.text(50, 25, 'Eqn: y=' + str(round(m[iter], 4)) + '*x+' + str(round(b[iter], 4)), fontsize=15) # Text displays y=mx+b on plot
 
 
# # Function updates data for plot animation using animation.FuncAnimation() below
# # The variable that is passed to this function from FuncAnimation is frames=itersteps-1
# # This acquires the data at every iteration step
# def update(iter):
#     y = m[iter] * x + b[iter]  # The linear fit data at each iteration using m and b values at that iteration
#     line.set_data(x, y)  # Updates linear fit data for plot
#     t1.set_text('Eqn: y=' + str(round(m[iter], 4)) + '*x+' + str(round(b[iter], 4)))
#     ax.set_title('Linear Regression with $R^2=$' + str(round(R_sq[iter], 4)) + ' iteration: ' + str(iter))
#     ax.legend(bbox_to_anchor=(1, 1.2), fontsize='x-small')  # legend location and font
#     return line, ax
 
 
# # Animation function after all the variables at each iteration have been calculated
# # Calls the function update and passes in the number of frames=itersteps-1 to get all the data at each iteration
# ani = animation.FuncAnimation(fig1, update, frames=itersteps - 1, interval=10, blit=False, repeat_delay=100)
# # ani.save('filename.gif',writer=writergif)

# writergif = animation.PillowWriter(fps=30)


# ani.save('lin_reg.mp4', writer=writergif)  # Saves animation
 
# # Figure of errors and coefficient of determination
# R_sq0=np.where(R_sq>0) # Finds indices of where Rsq>0
 
# fig2, ax2 = plt.subplots(figsize=(10, 10))
 
# ax2.plot(np.arange(R_sq0[0][0], itersteps - 1), SSE[R_sq0[0][0]:-1], label='SSE', color='blue')
# ax2.plot(np.arange(R_sq0[0][0], itersteps - 1), SSR[R_sq0[0][0]:-1], label='SSR', color='#0080ff')
# ax2.plot(np.arange(R_sq0[0][0], itersteps - 1), SSTO[R_sq0[0][0]:-1], label='SSTO', color='#00c0ff')
 
# ax2.set_title('Errors')
# ax2.set_xlabel('Number of Iterations')
# ax2.set_ylabel('Error', color='blue')
# ax2.tick_params('y', colors='blue')
 
# ax3 = ax2.twinx() # Second set of data on same x-axis
# ax3.plot(np.arange(R_sq0[0][0], itersteps - 1), R_sq[R_sq0[0][0]:-1], color='red', label='$R^2$')
# ax3.set_ylabel('Rsq', color='red')
# ax3.tick_params('y', colors='red')
 
# ax2.legend(bbox_to_anchor=(1, .60), fontsize='x-small')  # legend location and font size
# ax3.legend(bbox_to_anchor=(1, .50), fontsize='x-small')  # legend location and font size
# fig2.savefig('errors.png')  # saves figure














#WORKING

degree = 2
poly_model = PolynomialFeatures(degree=2)
poly_x_values = poly_model.fit_transform(x_values)

print ("initial values mapped")

poly_model.fit(poly_x_values, y_values)

regression_model = LinearRegression()
regression_model.fit(poly_x_values, y_values)

y_pred = regression_model.predict(poly_x_values)

print(regression_model.coef_)
regression_model.coef_


mean_squared_error(y_values, y_pred, squared=False)

num_degrees = [1,3,5,7,9]
plt_mean_squared_error = []

best_model = regression_model
best_poly = poly_model


for degree in num_degrees:
	print (degree)

	poly_model = PolynomialFeatures(degree=degree, include_bias=True)

	poly_x_values = poly_model.fit_transform(x_values)
	poly_model.fit(poly_x_values, y_values)

	regression_model = LinearRegression()
	regression_model.fit(poly_x_values, y_values)
	y_pred = regression_model.predict(poly_x_values)

	print(len(y_pred))


	# plt.plot(y_test, color="red") 
	# plt.plot(y_pred, color="blue") 

	if degree == 5:

		best_model = regression_model
		best_poly = poly_model

		print(best_model)
		print(best_poly)

		min_price = min(price)
		diff = (max(price) - min(price)) /2 
		for i in range(len(price)): 
			z = price[i]
			price[i] = z - diff - min_price

		# plt.plot(y_values, color="red") 
		# plt.plot(y_pred, color="blue") 
		# plt.plot(price/5, color="black")
		plt.plot(y_values, color='red')
		plt.plot(y_pred, color='blue')
		plt.show()


	plt_mean_squared_error.append(mean_squared_error(y_values, y_pred, squared=False))
  
print(plt_mean_squared_error)

# plt.scatter(num_degrees,plt_mean_squared_error, color="green")
# plt.plot(num_degrees,plt_mean_squared_error, color="red") 
# plt.show()



plt.scatter(x_values,y_values, color='red')
plt.plot(x_values,lin_reg.predict(poly_x_values[:,1:]), color='blue')
plt.show()

	
# print ("degree 5")

# poly_x_values = best_poly.fit_transform(x_test)

# # x_train2 = poly.fit_transform(x_values)
# # x_test2 = poly.fit_transform(x_test)

# # model = linear_model.LinearRegression()
# # model.fit(X_train, y_train)




# best_model.fit(poly_x_values, y_test)
# y_pred = best_model.predict(poly_x_values)

# print(len(y_pred))

# # plt.plot(y_test, color="red") 
# # plt.plot(y_pred, color="blue") 


# min_price = min(price)
# diff = (max(price) - min(price)) /2 
# for i in range(len(price)): 
# 	z = price[i]
# 	price[i] = z - diff - min_price

# print(mean_squared_error(y_test, y_pred, squared=True))

# plt.plot(y_test, color="red") 
# plt.plot(y_pred, color="blue") 
# plt.plot(price/5, color="black")


# plt.show()
# # print(mean_squared_error(y_test, y_pred, squared=True))





# # make sure to import all of our modules
# # sklearn package
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# # dataframes
# import pandas as pd
# # computation
# import numpy as np
# # visualization
# import matplotlib.pyplot as plt

# # dataset
# # https://www.kaggle.com/datasets/ciphernine/brooklyn-real-estate-listings
# # place it in the same folder as this workbook
# df = pd.read_csv('processed/data1.csv')

# # for this example, we're going to estimate the price with sqft, bathroom, and bedrooms
# df = df[[str(i) for i in range(541)]].dropna()

# # show some random lines from our data
# print(df.sample(n=15))

# x_values = df[[str(i) for i in range(540)]].values
# y_values = df['540'].values

# degree = 2
# poly_model = PolynomialFeatures(degree=2)
# poly_x_values = poly_model.fit_transform(x_values)

# print ("initial values mapped")

# poly_model.fit(poly_x_values, y_values)

# regression_model = LinearRegression()
# regression_model.fit(poly_x_values, y_values)

# y_pred = regression_model.predict(poly_x_values)

# regression_model.coef_


# mean_squared_error(y_values, y_pred, squared=False)

# num_degrees = [1,2,3,4,5,6,7]
# plt_mean_squared_error = []



# for degree in num_degrees:

#    poly_model = PolynomialFeatures(degree=degree)
  
#    poly_x_values = poly_model.fit_transform(x_values)
#    poly_model.fit(poly_x_values, y_values)
  
#    regression_model = LinearRegression()
#    regression_model.fit(poly_x_values, y_values)
#    y_pred = regression_model.predict(poly_x_values)

#    plt_mean_squared_error.append(mean_squared_error(y_values, y_pred, squared=False))
  
# plt.scatter(number_degrees,plt_mean_squared_error, color="green")
# plt.plot(number_degrees,plt_mean_squared_error, color="red") 

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