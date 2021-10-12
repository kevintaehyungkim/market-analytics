
import sched
import sys
import time
import pprint

import numpy as np
import api.yahoo_finance as yfin_api
# import utils as utils

# pp = pprint.PrettyPrinter(indent=4)

'''
Given stock symbol and number of days to limit option expiry,
returns all implied prices for the symbol based on available option expiry dates.
'''
def find_all_implied_prices(symbol, start, end=90):
	option_data = yfin_api.get_option_data(symbol, end)
	implied_prices = {}

	print('\nSymbol: ', symbol)
	print('Current Price: ${:0.2f}'.format(option_data[0]))

	for expiry_timestamp in option_data[1]:
		option_data = find_implied_price(symbol, expiry_timestamp)
		implied_prices[option_data[0]]=option_data[1:]

	# s = sched.scheduler(time.time, time.sleep)
	# s.enter(600, 1, find_all_implied_prices, (symbol, start, end,))
	# s.run()

	return implied_prices


'''
Given stock symbol and option expiry date (unix timestamp),
returns the implied price for the symbol based on the option chain.
'''
def find_implied_price(symbol, exp_timestamp):
	option_chain = yfin_api.get_option_chain(symbol, exp_timestamp)
	exp_time = time.localtime(exp_timestamp)
	exp_time_formatted = time.strftime("%m-%d-%Y", exp_time)

	symbol_expiry = symbol + ' ' + exp_time_formatted
	header = '*'*len(symbol_expiry)

	print('\n' + header)
	print(symbol_expiry)
	print(header)

	vol_stats = calculate_volume_stats(option_chain[0], option_chain[1])
	oi_stats = calculate_oi_stats(option_chain[0], option_chain[1])

	optimal_expiry_price = find_optimal_expiry_price(option_chain[0], option_chain[1])

	return [exp_time_formatted, oi_stats, vol_stats, optimal_expiry_price]



'''
Given call chain and put chain for an option expiry date, 
returns the optimal expiry price for MMs to pay out least in premiums.
'''
def find_optimal_expiry_price(call_chain, put_chain):
	expiry_strikes = [contract['strike'] for contract in call_chain]
	min_strike, max_strike = min(expiry_strikes), max(expiry_strikes)
	expiry_price_range = np.arange(min_strike, max_strike, 0.2).round(2).tolist()

	premiums_paid = {}

	call_oi = find_option_chain_oi(call_chain)
	put_oi = find_option_chain_oi(put_chain)

	for exp_price in expiry_price_range:
		premium_paid = 0
		for call_strike in call_oi:
			if call_strike < exp_price:
				premium_paid += (exp_price-call_strike)*call_oi[call_strike]*100

		for put_strike in put_oi:
			if put_strike > exp_price:
				premium_paid += (put_strike-exp_price)*put_oi[put_strike]*100

		premiums_paid[exp_price] = premium_paid

	lowest_prem_strikes = find_min_element_keys(premiums_paid, 5)
	lowest_prem_strike = lowest_prem_strikes[0]
	print ('MM Optimal Expiry: ${:.2f}'.format(lowest_prem_strike))
	# print('> ' + str(lowest_prem_strikes))

	return (lowest_prem_strike, premiums_paid)


def find_estimated_range():
	return


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
def calculate_oi_stats(call_chain, put_chain):
	sum_calls, call_contract_count = 0, 0
	sum_puts, put_contract_count = 0, 0

	call_strikes_oi = {}
	put_strikes_oi = {}

	call_strikes_oi_all = {}
	put_strikes_oi_all = {}

	for call in call_chain:
		strike_price = call['strike']
		strike_oi, ask_price = call.get('openInterest', 0), call.get('ask', 0)
		call_strikes_oi_all[str(strike_price)] = strike_oi

		if strike_oi > 0 and ask_price > 0.1:
			sum_calls += strike_price * strike_oi
			call_contract_count += strike_oi
			call_strikes_oi[str(strike_price)] = strike_oi

	for put in put_chain:
		strike_price = put['strike']
		strike_oi, ask_price = put.get('openInterest', 0), put.get('ask', 0)
		put_strikes_oi_all[str(strike_price)] = strike_oi

		if strike_oi > 0 and ask_price > 0.1:
			sum_puts += put['strike'] * strike_oi
			put_contract_count += strike_oi
			put_strikes_oi[str(strike_price)] = strike_oi

	call_oi_implied_price = sum_calls/call_contract_count
	put_oi_implied_price = sum_puts/put_contract_count
	total_contract_count = call_contract_count+put_contract_count

	oi_implied_price = (sum_calls+sum_puts)/total_contract_count

	print ('OI implied value: ${:.2f}'.format(oi_implied_price))
	print ('> Call OI implied value: ${:.2f}'.format(call_oi_implied_price) + ' | ' + str(call_contract_count) + ' contracts')
	print ('> Put OI implied value: ${:.2f}'.format(put_oi_implied_price) + ' | ' + str(put_contract_count) + ' contracts')
	print ('> Calls: ' + calculate_percent_string(call_contract_count,total_contract_count) + ' | Puts: ' + calculate_percent_string(put_contract_count,total_contract_count))

	print('Call Walls: ')
	most_traded_call_strikes = find_most_traded_strikes(call_strikes_oi)
	for cs in most_traded_call_strikes:
		print('> $' + cs + ': ' + str(call_strikes_oi[cs]))

	print('Put Walls: ')
	most_traded_put_strikes = find_most_traded_strikes(put_strikes_oi)
	for ps in most_traded_put_strikes:
		print('> $' + ps + ': ' + str(put_strikes_oi[ps]))

	return [oi_implied_price, (most_traded_call_strikes, call_strikes_oi_all), (most_traded_put_strikes, put_strikes_oi_all)]


'''
Calculates implied price based on all strike price and volume in the option chain
'''
def calculate_volume_stats(call_chain, put_chain):
	sum_calls, call_contract_count = 0, 0
	sum_puts, put_contract_count = 0, 0

	for call in call_chain:
		strike_call_volume, call_ask_price = call.get('volume', 0), call.get('ask', 0)
		if strike_call_volume > 0 and call_ask_price > 0.1:
			sum_calls += call['strike'] * strike_call_volume
			call_contract_count += strike_call_volume

	for put in put_chain:
		strike_put_volume, put_ask_price = put.get('volume', 0), put.get('ask', 0)
		if strike_put_volume > 0 and put_ask_price > 0.1:
			sum_puts += put['strike'] * strike_put_volume
			put_contract_count += strike_put_volume

	call_vol_implied_price = sum_calls/call_contract_count
	put_vol_implied_price = sum_puts/put_contract_count
	total_contract_count = call_contract_count+put_contract_count

	vol_implied_price = (sum_calls+sum_puts)/total_contract_count

	print ('Volume implied value: ${:.2f}'.format(vol_implied_price))
	print ('> Call volume implied value: ${:.2f}'.format(call_vol_implied_price) + ' | ' + str(call_contract_count) + ' contracts')
	print ('> Put volume implied value: ${:.2f}'.format(put_vol_implied_price) + ' | ' + str(put_contract_count) + ' contracts')
	print ('> Calls: ' + calculate_percent_string(call_contract_count,total_contract_count) + ' | Puts: ' + calculate_percent_string(put_contract_count,total_contract_count))

	return vol_implied_price




def find_option_chain_oi(option_chain):
	strike_oi = {}

	for contract in option_chain:
		strike = contract['strike']
		oi = contract.get('openInterest', 0)
		strike_oi[strike] = oi

	return strike_oi

def find_most_traded_strikes(strike_contracts, limit=5):
	return sorted(strike_contracts, key=strike_contracts.get, reverse=True)[:limit]


# utils
def find_min_element_keys(data, limit=5):
	return sorted(data, key=data.get, reverse=False)[:limit]

def find_max_element_keys(limit=5):
	return sorted(data, key=data.get, reverse=True)[:limit] 

def calculate_percent_string(num, denom):
	return "{0:.0%}".format(num/denom)


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
'''
Usage: 

python3 option_analytics.py SPY
python3 option_analytics.py QQQ
'''

# find_all_implied_prices(sys.argv[1], 0, 5)


