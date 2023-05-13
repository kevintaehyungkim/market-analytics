# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import api.api_utils as api_utils
import data.data_loader as data
import numpy as np

DATA_MAP = data.DATA_MAP


'''
- macd cross earlier then check 1 timestamp below

1. DAILY MACD cross
2. macd signal cross with overbought/oversold line +/- 6.5
3. macd signal cross with overbought/oversold line +/- 6.5 and rsi mid line
3. macd zero cross + overbought or oversold line 
3. macd cross + overbought or oversold line + 100 ema
2. MACD + EMA 100 + RSI mid


macD 
- 100day EMA 


buy below rsi signal line + macd crossover up vice versa
'''

# DEFAULT VALUES
RSI_MID = 50
THETA = 0.0005 # adjust later to log

MARKET_DATES = data.MARKET_DATES
MARKET_DATES.reverse()
NUM_DATES = len(MARKET_DATES)


DAILY_DATA = data.SPY_DAILY #ticker_timeframe
MACD_DATA = data.SPY_MACD #ticker_timeframe
RSI_DATA = data.SPY_RSI #ticker_timeframe


# SPY # 
SPY_1H_TIMESTAMPS = data.SPY_1H_TIMESTAMPS
SPY_1H_PRICES = data.SPY_1H_PRICES
SPY_1H_MACD = data.SPY_1H_MACD
SPY_1H_RSI = data.SPY_1H_RSI

SPY_1H_EMA100 = data.SPY_1H_EMA100
SPY_1H_EMA200 = data.SPY_1H_EMA200

SPY_1H_EMA100_2 = data.SPY_1H_EMA100_2
SPY_1H_EMA200_2 = data.SPY_1H_EMA200_2

SPY_1H_TOTAL = len(SPY_1H_TIMESTAMPS)


zzzp = []
zzzema200 = []
zzzmacd = []
zzzsignal = []


def strategy_4(profit_target, stop_target, trade_window, verification_window, macd_range):
	val = 1000
	vals = []
	wins, trades = 0, 0

	macd = macd_signal_cross(SPY_1H_MACD, SPY_1H_TIMESTAMPS[0]) # 1 signal above value line
	rsi_dir = rsi_signal_cross(SPY_1H_RSI, SPY_1H_TIMESTAMPS[0])

	ema200_val = SPY_1H_EMA200[SPY_1H_TIMESTAMPS[0]]

	macd_history = []
	rsi_history = []
	
	i = 1
	while i < SPY_1H_TOTAL - (trade_window+verification_window+1):

		# check conditions
		curr_macd = macd_signal_cross(SPY_1H_MACD, SPY_1H_TIMESTAMPS[i])
		date = SPY_1H_TIMESTAMPS[i]
		
		macd_val = SPY_1H_MACD[date]['value']
		macd_signal_val = SPY_1H_MACD[date]['signal']
		macd_histogram_val = SPY_1H_MACD[date]['histogram']
		
		curr_rsi_dir = rsi_signal_cross(SPY_1H_RSI, SPY_1H_TIMESTAMPS[i])
		rsi_val = SPY_1H_RSI[date]['rsi']
		rsi_sma14_val = SPY_1H_RSI[date]['rsi_14sma']

		curr_price = SPY_1H_PRICES[date]['close']
		curr_ema200_val = SPY_1H_EMA200[date]

		# ENTRY CONSIDERATION TRIGGER  (verification -> sell trigger)
		# RSI cross -> need 3 continuous verification on both RSI and MACD in direction (or macd cross of at least 1.25 range -> rsi and macd confirms direction 
		# exit -> RSI switches direction
		# ADX
		# Livermore's Pivotal Points

		# TRIGGER 1: RSI x RSI 14d SMA Crossover
		if curr_rsi_dir != rsi_dir: #rename new and curr

			rsi_val_ver = [rsi_val]
			rsi_hist_ver = [rsi_val - rsi_sma14_val]
			macd_hist_ver = [macd_histogram_val]
			signal_verified = 0

			j = i+1
			while j <= i + verification_window:

				date2 = SPY_1H_TIMESTAMPS[j]
				macd_val2 = SPY_1H_MACD[date2]['value']
				macd_hist2 = SPY_1H_MACD[date2]['histogram']
				rsi_val2 = SPY_1H_RSI[date2]['rsi']
				rsi_hist2 = SPY_1H_RSI[date2]['rsi'] - SPY_1H_RSI[date2]['rsi_14sma']
				macd2 = macd_signal_cross(SPY_1H_MACD, SPY_1H_TIMESTAMPS[j])

				# print ("\n")
				# print("rsi dir now: " + str(curr_rsi_dir))
				# print("macd dir at switch: " + str(macd))

				# print("macd now: " + str(macd2))
				# print("macd hist: " + str(macd_hist_ver))
				# print("rsi hist: " + str(rsi_hist_ver))

				# print("macd now: " + str(macd_hist2))
				# print("rsi now: " + str(rsi_hist2))

				# print(macd2)

				if j < i + verification_window:
					if curr_rsi_dir == 1:
						if macd_hist2 < macd_hist_ver[-1]: # perhaps or macd signal 
							break 
					elif curr_rsi_dir == -1:
						if macd_hist2 > macd_hist_ver[-1]:
							break 
				else:
					if curr_rsi_dir == macd2 and abs(macd_val2) >= macd_range:
						if curr_rsi_dir == 1 and rsi_val2 < 45:
							signal_verified = 1
						elif curr_rsi_dir == -1 and rsi_val2 > 55:
							signal_verified = -1

				# rsi_val_ver.append()
				rsi_hist_ver.append(rsi_hist2)
				macd_hist_ver.append(macd_hist2)

				j += 1

			# Execute Trade
			if signal_verified != 0:
				k = j + 1
				entry_date = SPY_1H_TIMESTAMPS[k]
				entry = SPY_1H_PRICES[entry_date]['open']
				# TRADE PERIOD #

				# if signal_verified == 1 and 

		
				while k < j + 1 + trade_window:
					# print(k)
					# if k%8 == 0:
					# 	val *= 1-THETA

					trade_days = k - j

					curr_date = SPY_1H_TIMESTAMPS[k]
					high, low = SPY_1H_PRICES[curr_date]['high'], SPY_1H_PRICES[curr_date]['low']

					val_k = check_trade(curr_rsi_dir, val, entry, high, low, profit_target, stop_target)
					# print(val_k)

					# add sell trigger

					if val_k is not None:
						if val_k > val:
							wins += 1

						val = val_k
						# print(val)
						break

					if trade_days == trade_window:
						val *= (1 - THETA*trade_days)

					k += 1

				trades += 1

		# else if (rsi_crossover):
				# TRADE PERIOD #

		macd = curr_macd
		rsi_dir = curr_rsi_dir
		curr_ema200_val = curr_ema200_val
		vals.append(val)

		# macd_history = add_history(SPY_1H_MACD[date], macd_history, macd_history_window)
		# rsi_history = add_history(SPY_1H_RSI[date], macd_history, macd_history_window)

		i += 1

	# print("STRATEGY 4")
	print("val: " + str(val))

	if trades == 0:
		trades = 1
		wins = -1


	print("win %: " + str((wins/trades)*100) + " (" + str(wins) + " wins " + str(trades-wins) + " losses)")
	print("\n")	

	return val, (wins/trades)*100, trades


def add_history(val, history_arr, window):
	if len(history_arr) >= window:
		history_arr.pop(0)

	history_arr.append(val)
	return history_arr
         

def macd_signal_cross(macd_data, date):
	if macd_data[date]['histogram'] >= 0:
		return 1
	else:
		return -1

def rsi_signal_cross(rsi_data, date):
	rsi = rsi_data[date]['rsi']
	rsi_14sma = rsi_data[date]['rsi_14sma']

	if rsi - rsi_14sma >= 0:
		return 1
	else:
		return -1

	# return int(macd['histogram']/abs(macd['histogram']))
                              
# def process_call(entry_date, entry)

# def process_put(entry_date, entry)

# call_w = 0
# put_w = 0

def check_trade(trade, val, entry, high, low, profit_target, stop_target):
	# calls
	new_val = val

	if trade == 1:
		profit_price = entry*profit_target
		stop_price = entry*stop_target

		# print("call entry: " + str(entry))
		# print("profit target: " + str(profit_target))
		# print("profit price: " + str(profit_price))
		# print("stop target: " + str(stop_target))
		# print("stop price: " + str(stop_price))

		if high >= profit_price:
			# new_val *= (1+(profit_target-1))
			print("w")
			return entry*profit_target
			# call_w += 1
		elif low <= stop_price:
			return val*stop_target
			# return val - val*(1-stop_diff2)
			# new_val *= 1-((1-stop_target)*5)
			# print("l: " + str(new_val))
			# return new_val
		else: 
			return None
	# puts
	else:
		profit_price = entry-entry*(profit_target-1)
		stop_price = entry+entry*(1-stop_target)

		# print("put entry: " + str(entry))
		# print("profit target: " + str(profit_target))
		# print("profit price: " + str(profit_price))
		# print("stop target: " + str(stop_target))
		# print("stop price: " + str(stop_price))

		if low <= profit_price:
			print("w")
			return val * profit_target
			# put_w += 1
		elif high >= stop_price:
			return val*stop_target

			# return val - val*(1-stop_diff2)
			# print("l: " + str(new_val))
			# return new_val
		else:
			return None



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

def load_json(filepath): 
	f = open(filepath)
	data = json.load(f) 
	return data



# trading_window = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 100]
# min_profits = [1.01, 1.02, 1.03, 1.04]
# min_losses = [.99, 0.98, .97, 0.96, 0.95]
# verification_windows = [1, 2, 3]
# macd_ranges = [0.5, 1, 1.5, 2]

# vals = []
# win_ratios = []

# for t in trading_window:
# 	for p in min_profits:
# 		print(t, p)
# 		for l in min_losses:
# 			for vw in verification_windows:
# 				for r in macd_ranges: 
# 					test = "t: " + str(t) + " p: " + str(p) + " l: " + str(l) + " vw: " + str(vw) + " r: " + str(r)
# 					print(test)
# 					val, win_percent, trades = strategy_4(p, l, t, vw, r)
# 					win_ratios.append((win_percent, val, trades, test))
# 					vals.append((val, win_percent, trades, test))

# vals.sort(reverse=True)
# win_ratios.sort(reverse=True)

# top_winners = vals[:40]
# top_win_ratios = win_ratios[:40]

# vals.sort()
# top_losers = vals[:40]

# print("\n")
# print("most gain")
# for w in top_winners:
# 	print(w)

# print("\n")
# print("most loss")
# for l in top_losers:
# 	print(l)

# print("\n")
# print("highest win percents")
# for w in top_win_ratios: 
# 	print(w)

# print("\n")
# just_vals = []

# for v in vals:
# 	just_vals.append(v[0])

# avg_val = sum(just_vals)/len(just_vals)
# print("avg val: " + str(avg_val))




# zzzp1 = np.array(zzzp)
# zzzema2001 = np.array(zzzema200)
# zzzmacd1 = np.array(zzzmacd)
# zzzsignal1 = np.array(zzzsignal)

# zzzp2 = zzzp1[200:]
# zzzema2002 = zzzema2001[200:]
# zzzmacd2 = zzzmacd1[200:]
# zzzsignal2 = zzzsignal1[200:]


 # 81, 't: 8 p: 1.04 l: 0.99 vw: 2 r: 2')


val, win_percent, trades = strategy_4(1.04,0.99,8,2,2)

# print(val)
# print(win_percent)
# print(trades)

# strategy_4(80,1.9,0.95,2,1.5)
# print(call_w)
# print(put_w)

import matplotlib.pyplot as plt

# plt.plot(zzzp2/(max(zzzp2)*8))
# plt.plot(zzzema2002/(max(zzzema2002)*8))
# plt.plot(zzzmacd2)
# plt.plot(zzzsignal2)
# plt.show()



macddd = []
macddd_signal = []
rsiii = []
rsiii_14sma = []
priceee = []
emaaa100 = []
emaaa200 = []
emaaa100_2 = []
emaaa200_2 = []

print(SPY_1H_TIMESTAMPS[-200])

for t in SPY_1H_TIMESTAMPS:
	macddd.append(SPY_1H_MACD[t]['value'])
	macddd_signal.append(SPY_1H_MACD[t]['signal'])
	rsiii.append(SPY_1H_RSI[t]['rsi'])
	rsiii_14sma.append(SPY_1H_RSI[t]['rsi_14sma'])
	priceee.append(SPY_1H_PRICES[t]['close'])
	
	emaaa100.append(SPY_1H_EMA100[t])
	emaaa200.append(SPY_1H_EMA200[t])
	emaaa100_2.append(SPY_1H_EMA100_2[t])
	emaaa200_2.append(SPY_1H_EMA100_2[t])

print (len(macddd))
print(len(rsiii))

max_rsiii = max(rsiii)
max_priceee = max(priceee)

# for i in range(len(rsiii)):
# 	r = rsiii[i]
# 	new_r = r/max_rsiii
# 	rsiii[i] = new_r

for i in range(len(priceee)):
	r = priceee[i]
	new_r = r/8
	priceee[i] = new_r



# print(SPY_1H_TIMESTAMPS[17500])

# Set the theme of our chart
plt.style.use('fivethirtyeight')

# Make our resulting figure much bigger
plt.rcParams['figure.figsize'] = (15, 7)


# plt.plot(macddd[-100:], color='blue')
# plt.plot(macddd_signal[-100:], color='red')
plt.plot(rsiii[-1000:], color='purple', linewidth=1)
plt.plot(rsiii_14sma[-1000:], color='yellow', linewidth=1)
# plt.plot(priceee[-100:], color='black')
# plt.plot(emaaa100[-200:], color='green')
# plt.plot(emaaa200[-200:], color='blue')
# plt.plot(emaaa100_2[-200:], color='orange')
# plt.plot(emaaa200_2[-200:], color='red')

plt.show()

