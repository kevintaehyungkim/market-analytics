import sys
import time

import api.yahoo_finance as yfin_api
# import utils as utils

CALL=''

'''
Given stock symbol and number of days to limit option expiry,
returns all implied prices for the symbol based on available option expiry dates.
'''
def find_all_implied_prices(symbol, start, end=180):
	option_data = yfin_api.get_option_data(symbol, end)
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
		strike_call_oi, call_ask_price = call.get('openInterest', 0), call.get('ask', 0)
		if strike_call_oi > 0 and call_ask_price > 0.05:
			sum_calls += call['strike'] * strike_call_oi
			call_contract_count += strike_call_oi

	for put in put_chain:
		strike_put_oi, put_ask_price = put.get('openInterest', 0), put.get('ask', 0)
		if strike_put_oi > 0 and put_ask_price > 0.05:
			sum_puts += put['strike'] * strike_put_oi
			put_contract_count += strike_put_oi

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
		strike_call_volume, call_ask_price = call.get('volume', 0), call.get('ask', 0)
		if strike_call_volume > 0 and call_ask_price > 0.05:
			sum_calls += call['strike'] * strike_call_volume
			call_contract_count += strike_call_volume

	for put in put_chain:
		strike_put_volume, put_ask_price = put.get('volume', 0), put.get('ask', 0)
		if strike_put_volume > 0 and put_ask_price > 0.05:
			sum_puts += put['strike'] * strike_put_volume
			put_contract_count += strike_put_volume

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

find_all_implied_prices('SPY', 0, 60)





