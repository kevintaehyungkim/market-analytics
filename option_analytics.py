import sys
import time

import api.yahoo_finance as yfin
# import utils as utils



'''
Calculates option chain implied price based on all strike prices and open-interest in the option chain

'''
def calculate_oi_implied_price(call_chain, put_chain):
	sum_calls, call_oi = 0, 0
	sum_puts, put_oi = 0, 0

	for call in call_chain:
		sum_calls += call['strike']*call.get('openInterest', 0)
		call_oi += call.get('openInterest', 0)

	for put in put_chain:
		sum_puts += put['strike']*put.get('openInterest', 0)
		put_oi += put.get('openInterest', 0)

	call_oi_implied_price = sum_calls/call_oi
	put_oi_implied_price = sum_puts/put_oi
	oi_implied_price = (sum_calls+sum_puts)/(call_oi+put_oi)



	print ('OI implied value: ${:.2f}'.format(oi_implied_price))
	print ('-> Call OI implied value: ${:.2f}'.format(call_oi_implied_price) + ' | #contracts: ' + str(call_oi))
	print ('-> Put OI implied value: ${:.2f}'.format(put_oi_implied_price) + ' | #contracts: ' + str(put_oi))

	return oi_implied_price


'''
Calculates option chain implied price based on all strike price and volume in the option chain
'''
def calculate_vol_implied_price(call_chain, put_chain):
	sum_calls, call_vol = 0, 0
	sum_puts, put_vol = 0, 0

	for call in call_chain:
		sum_calls += call['strike']*call.get('volume', 0)
		call_vol += call.get('volume', 0)

	for put in put_chain:
		sum_puts += put['strike']*put.get('volume', 0)
		put_vol += put.get('volume', 0)

	call_vol_implied_price = sum_calls/call_vol
	put_vol_implied_price = sum_puts/put_vol
	vol_implied_price = (sum_calls+sum_puts)/(call_vol+put_vol)

	print ('Volume implied value: ${:.2f}'.format(vol_implied_price))
	print ('-> Call volume implied value: ${:.2f}'.format(call_vol_implied_price) + ' | #contracts: ' + str(call_vol))
	print ('-> Put volume implied value: ${:.2f}'.format(put_vol_implied_price) + ' | #contracts: ' + str(put_vol))

	return vol_implied_price


def find_implied_price(symbol, expiry_limit_days):
	option_data = yfin.get_option_data(symbol, expiry_limit_days)
	contract_implied_prices = {}

	print('\nSymbol: ', symbol)
	print('Current Price: ${:0.2f}'.format(option_data[0]))

	for exp_date in option_data[1]:
		option_chain = yfin.get_option_chain(symbol, exp_date)
		exp_time = time.localtime(exp_date)
		exp_time_formatted = time.strftime("%Y-%m-%d", exp_time)

		print('\n[' + exp_time_formatted + ']')
		vol_implied_price = calculate_vol_implied_price(option_chain[0], option_chain[1])
		oi_implied_price = calculate_oi_implied_price(option_chain[0], option_chain[1])

		contract_implied_prices[exp_time_formatted]=(vol_implied_price, oi_implied_price)

	return


'''
Given stock symbol, target price, and target date for that price,
finds the 5 most profitable option contracts.

For now let's assume IV is constant.
Yahoo Finance API is a starting point
'''
def find_optimal_contracts(symbol, target_price, target_date):
	return









# '''
# Filter expiry dates for number of days into the future - defaults to 90 days
# '''
# def filter_expiry_timestamps(expiry_timestamps, days=400):
# 	curr_timestamp = int(time.time())
# 	filter_timestamp = curr_timestamp + days*86400

# 	return [exp for exp in expiry_timestamps if exp <= filter_timestamp]



########################
### temporary script ###
########################

find_implied_price('SPY', 90)


# STOCK = "GLD"

# option_data = yfin.get_option_data(STOCK)

# print('\n')
# print('Symbol: ', STOCK)
# print('Current Price: ${:0.2f}'.format(option_data[0]))


# for exp_date in option_data[1]:
# 	option_chain = yfin.get_option_chain(STOCK, exp_date)
# 	exp_time = time.localtime(exp_date)

# 	print('\n[' + time.strftime("%Y-%m-%d", exp_time) + ']')
# 	vol_implied_price = calculate_vol_implied_price(option_chain[0], option_chain[1])
# 	oi_implied_price = calculate_oi_implied_price(option_chain[0], option_chain[1])

