import finnhub


finnhub_client = finnhub.Client(api_key="c4m7j62ad3icjh0edqtg")

print(finnhub_client.support_resistance('AAPL', 'D'))


'''
Get support and resistance levels for a symbol.

symbol (req): 
	stock symbol
resolution (req):
	Supported resolution includes 1, 5, 15, 30, 60, D, W, M.
	Some timeframes might not be available depending on the exchange.
'''
def get_support_resistance(symbol, timeframe):
	return