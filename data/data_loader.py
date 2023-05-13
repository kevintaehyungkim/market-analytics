import json
import sys

sys.path.append('../')


# DIA - dow jones
# IYT = dow jones transportation
# UUP = USD

tickers = ['SPY', 'DIA', 'IYT', 'VXX', 'UUP', 'JNK', 'IEF', 'TLT', 'OILK', 'GLD']
data_map = []


def load_json(filepath): 
	f = open(filepath)
	data = json.load(f) 
	return data


MARKET_DATES = load_json('raw/stock_dates.json')

SPY_DAILY = load_json('raw/SPY_daily_data.json')
SPY_20EMA = load_json('raw/SPY_20ema_data.json')
SPY_50EMA = load_json('raw/SPY_50ema_data.json')
SPY_100EMA = load_json('raw/SPY_100ema_data.json')
# SPY_200EMA = load_json('raw/SPY_200ema_data.json')
SPY_MACD = load_json('raw/SPY_macd_data.json')
SPY_RSI = load_json('raw/SPY_rsi_data.json')

SPY_1H_TIMESTAMPS = load_json('raw/SPY/1h/timestamps.json')
SPY_1H_PRICES = load_json('raw/SPY/1h/prices.json')
SPY_1H_MACD = load_json('raw/SPY/1h/macd2.json')
SPY_1H_RSI = load_json('raw/SPY/1h/rsi.json')

SPY_1H_EMA100 = load_json('raw/SPY/1h/100ema.json')
SPY_1H_EMA200 = load_json('raw/SPY/1h/200ema.json')

SPY_1H_EMA100_2 = load_json('raw/SPY/1h/100ema2.json')
SPY_1H_EMA200_2 = load_json('raw/SPY/1h/200ema2.json')



DIA_DAILY = load_json('raw/DIA_daily_data.json')
DIA_20EMA = load_json('raw/DIA_20ema_data.json')
DIA_50EMA = load_json('raw/DIA_50ema_data.json')
DIA_100EMA = load_json('raw/DIA_100ema_data.json')
# DIA_200EMA = load_json('raw/DIA_200ema_data.json')
DIA_MACD = load_json('raw/DIA_macd_data.json')
DIA_RSI = load_json('raw/DIA_rsi_data.json')


IYT_DAILY = load_json('raw/IYT_daily_data.json')
IYT_20EMA = load_json('raw/IYT_20ema_data.json')
IYT_50EMA = load_json('raw/IYT_50ema_data.json')
IYT_100EMA = load_json('raw/IYT_100ema_data.json')
# IYT_200EMA = load_json('raw/IYT_200ema_data.json')
IYT_MACD = load_json('raw/IYT_macd_data.json')
IYT_RSI = load_json('raw/IYT_rsi_data.json')


VXX_DAILY = load_json('raw/VXX_daily_data.json')
VXX_20EMA = load_json('raw/VXX_20ema_data.json')
VXX_50EMA = load_json('raw/VXX_50ema_data.json')
VXX_100EMA = load_json('raw/VXX_100ema_data.json')
# VXX_200EMA = load_json('raw/VXX_200ema_data.json')
VXX_MACD = load_json('raw/VXX_macd_data.json')
VXX_RSI = load_json('raw/VXX_rsi_data.json')


UUP_DAILY = load_json('raw/UUP_daily_data.json')
UUP_20EMA = load_json('raw/UUP_20ema_data.json')
UUP_50EMA = load_json('raw/UUP_50ema_data.json')
UUP_100EMA = load_json('raw/UUP_100ema_data.json')
# UUP_200EMA = load_json('raw/UUP_200ema_data.json')
UUP_MACD = load_json('raw/UUP_macd_data.json')
UUP_RSI = load_json('raw/UUP_rsi_data.json')


JNK_DAILY = load_json('raw/JNK_daily_data.json')
JNK_20EMA = load_json('raw/JNK_20ema_data.json')
JNK_50EMA = load_json('raw/JNK_50ema_data.json')
JNK_100EMA = load_json('raw/JNK_100ema_data.json')
# JNK_200EMA = load_json('raw/JNK_200ema_data.json')
JNK_MACD = load_json('raw/JNK_macd_data.json')
JNK_RSI = load_json('raw/JNK_rsi_data.json')


IEF_DAILY = load_json('raw/IEF_daily_data.json')
IEF_20EMA = load_json('raw/IEF_20ema_data.json')
IEF_50EMA = load_json('raw/IEF_50ema_data.json')
IEF_100EMA = load_json('raw/IEF_100ema_data.json')
# IEF_200EMA = load_json('raw/IEF_200ema_data.json')
IEF_MACD = load_json('raw/IEF_macd_data.json')
IEF_RSI = load_json('raw/IEF_rsi_data.json')


TLT_DAILY = load_json('raw/TLT_daily_data.json')
TLT_20EMA = load_json('raw/TLT_20ema_data.json')
TLT_50EMA = load_json('raw/TLT_50ema_data.json')
TLT_100EMA = load_json('raw/TLT_100ema_data.json')
# TLT_200EMA = load_json('raw/TLT_200ema_data.json')
TLT_MACD = load_json('raw/TLT_macd_data.json')
TLT_RSI = load_json('raw/TLT_rsi_data.json')


OILK_DAILY = load_json('raw/OILK_daily_data.json')
OILK_20EMA = load_json('raw/OILK_20ema_data.json')
OILK_50EMA = load_json('raw/OILK_50ema_data.json')
OILK_100EMA = load_json('raw/OILK_100ema_data.json')
# OILK_200EMA = load_json('raw/OILK_200ema_data.json')
OILK_MACD = load_json('raw/OILK_macd_data.json')
OILK_RSI = load_json('raw/OILK_rsi_data.json')


GLD_DAILY = load_json('raw/GLD_daily_data.json')
GLD_20EMA = load_json('raw/GLD_20ema_data.json')
GLD_50EMA = load_json('raw/GLD_50ema_data.json')
GLD_100EMA = load_json('raw/GLD_100ema_data.json')
# GLD_200EMA = load_json('raw/GLD_200ema_data.json')
GLD_MACD = load_json('raw/GLD_macd_data.json')
GLD_RSI = load_json('raw/GLD_rsi_data.json')

DATA_MAP = {
'SPY' : {'DAILY': SPY_DAILY, 'EMA20': SPY_20EMA, 'EMA50': SPY_50EMA, 'EMA100': SPY_100EMA, 'MACD': SPY_MACD, 'RSI': SPY_RSI },
'DIA' : {'DAILY': DIA_DAILY, 'EMA20': DIA_20EMA, 'EMA50': DIA_50EMA, 'EMA100': DIA_100EMA, 'MACD': DIA_MACD, 'RSI': DIA_RSI },
'IYT' : {'DAILY': IYT_DAILY, 'EMA20': IYT_20EMA, 'EMA50': IYT_50EMA, 'EMA100': IYT_100EMA, 'MACD': IYT_MACD, 'RSI': IYT_RSI },
'VXX' : {'DAILY': VXX_DAILY, 'EMA20': VXX_20EMA, 'EMA50': VXX_50EMA, 'EMA100': VXX_100EMA, 'MACD': VXX_MACD, 'RSI': VXX_RSI },
'UUP' : {'DAILY': UUP_DAILY, 'EMA20': UUP_20EMA, 'EMA50': UUP_50EMA, 'EMA100': UUP_100EMA, 'MACD': UUP_MACD, 'RSI': UUP_RSI },
'JNK' : {'DAILY': JNK_DAILY, 'EMA20': JNK_20EMA, 'EMA50': JNK_50EMA, 'EMA100': JNK_100EMA, 'MACD': JNK_MACD, 'RSI': JNK_RSI },
'IEF' : {'DAILY': IEF_DAILY, 'EMA20': IEF_20EMA, 'EMA50': IEF_50EMA, 'EMA100': IEF_100EMA, 'MACD': IEF_MACD, 'RSI': IEF_RSI },
'TLT' : {'DAILY': TLT_DAILY, 'EMA20': TLT_20EMA, 'EMA50': TLT_50EMA, 'EMA100': TLT_100EMA, 'MACD': TLT_MACD, 'RSI': TLT_RSI },
'OILK' : {'DAILY': OILK_DAILY, 'EMA20': OILK_20EMA, 'EMA50': OILK_50EMA, 'EMA100': OILK_100EMA, 'MACD': OILK_MACD, 'RSI': OILK_RSI },
'GLD' : {'DAILY': GLD_DAILY, 'EMA20': GLD_20EMA, 'EMA50': GLD_50EMA, 'EMA100': GLD_100EMA,'MACD': GLD_MACD, 'RSI': GLD_RSI },
}



# for ticker in tickers:
# 	print("\n")
# 	print (ticker + "_DAILY = " + "load_json('raw/" + ticker + "_daily_data.json')")
# 	print (ticker + "_20EMA = " + "load_json('raw/" + ticker + "_20ema_data.json')")
# 	print (ticker + "_50EMA = " + "load_json('raw/" + ticker + "_50ema_data.json')")
# 	print (ticker + "_100EMA = " + "load_json('raw/" + ticker + "_100ema_data.json')")
# 	print (ticker + "_MACD = " + "load_json('raw/" + ticker + "_macd_data.json')")
# 	print (ticker + "_RSI = " + "load_json('raw/" + ticker + "_rsi_data.json')")

# print ("data_map = {")
# for ticker in tickers:
# 	print ("'" + ticker + "' = " + "{'DAILY': " + ticker + "_DAILY, 'EMA20': " + ticker + "_20EMA, 'EMA50': " + ticker + "_50EMA, 'EMA100': " + ticker + "_100EMA, 'EMA200': " + ticker + "_200EMA, 'MACD': " + ticker + "_RSI, 'RSI': " + ticker + "_RSI },")
# print("}")
