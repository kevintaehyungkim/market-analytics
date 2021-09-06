import sys
import time

import api.yahoo_finance as yfin_api
# import utils as utils



'''
Given stock symbol and number of days to limit option expiry,
returns all implied prices for the symbol based on available option expiry dates.
'''
def find_all_implied_prices(symbol, expiry_limit_days=90):
	option_data = yfin_api.get_option_data(symbol, expiry_limit_days)
	implied_prices = {}

	print('\nSymbol: ', symbol)
	print('Current Price: ${:0.2f}'.format(option_data[0]))

	for expiry_timestamp in option_data[1]:
		implied_prices[expiry_timestamp]=find_implied_price(symbol, expiry_timestamp)

	return implied_prices


'''
Given stock symbol and option expiry date (unix timestamp),
returns the implied price for the symbol based on the option chain.
'''
def find_implied_price(symbol, exp_timestamp):
	option_chain = yfin_api.get_option_chain(symbol, exp_timestamp)
	exp_time = time.localtime(exp_timestamp)
	exp_time_formatted = time.strftime("%Y-%m-%d", exp_time)

	print('\n[' + exp_time_formatted + ']')
	vol_implied_price = calculate_vol_implied_price(option_chain[0], option_chain[1])
	oi_implied_price = calculate_oi_implied_price(option_chain[0], option_chain[1])

	return [vol_implied_price, oi_implied_price]


'''
Given stock symbol, target price, and target date for that price,
finds the 5 most profitable option contracts.

For now let's assume IV is constant.
Yahoo Finance API is a starting point
'''
def find_optimal_contracts(symbol, target_price, target_date):
	return



'''
Calculates implied price based on all strike prices and open-interest in the option chain
'''
def calculate_oi_implied_price(call_chain, put_chain):
	sum_calls, call_contract_count = 0, 0
	sum_puts, put_contract_count = 0, 0

	for call in call_chain:
		sum_calls += call['strike']*call.get('openInterest', 0)
		call_contract_count += call.get('openInterest', 0)

	for put in put_chain:
		sum_puts += put['strike']*put.get('openInterest', 0)
		put_contract_count += put.get('openInterest', 0)

	call_oi_implied_price = sum_calls/call_contract_count
	put_oi_implied_price = sum_puts/put_contract_count
	total_contract_count = call_contract_count+put_contract_count

	oi_implied_price = (sum_calls+sum_puts)/total_contract_count

	print ('OI implied value: ${:.2f}'.format(oi_implied_price))
	print ('-> Call OI implied value: ${:.2f}'.format(call_oi_implied_price) + ' | #contracts: ' + str(call_contract_count))
	print ('-> Put OI implied value: ${:.2f}'.format(put_oi_implied_price) + ' | #contracts: ' + str(put_contract_count))

	return oi_implied_price


'''
Calculates implied price based on all strike price and volume in the option chain
'''
def calculate_vol_implied_price(call_chain, put_chain):
	sum_calls, call_contract_count = 0, 0
	sum_puts, put_contract_count = 0, 0

	for call in call_chain:
		sum_calls += call['strike']*call.get('volume', 0)
		call_contract_count += call.get('volume', 0)

	for put in put_chain:
		sum_puts += put['strike']*put.get('volume', 0)
		put_contract_count += put.get('volume', 0)

	call_vol_implied_price = sum_calls/call_contract_count
	put_vol_implied_price = sum_puts/put_contract_count
	total_contract_count = call_contract_count+put_contract_count

	vol_implied_price = (sum_calls+sum_puts)/total_contract_count

	print ('Volume implied value: ${:.2f}'.format(vol_implied_price))
	print ('-> Call volume implied value: ${:.2f}'.format(call_vol_implied_price) + ' | #contracts: ' + str(call_contract_count))
	print ('-> Put volume implied value: ${:.2f}'.format(put_vol_implied_price) + ' | #contracts: ' + str(put_contract_count))

	return vol_implied_price





### TODO ###

'''
Given an option contract, calculate optimal stock price points for stop loss
'''
def calculate_optimal_stop_loss():
	return


'''
Given an option contract, calculate optimal stock price points for limit sell
'''
def calculate_optimal_limit_sell():
	return 





########################
### temporary script ###
########################

find_all_implied_prices('SPY', 90)





