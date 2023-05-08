# import finnhub


# finnhub_client = finnhub.Client(api_key="c4m7j62ad3icjh0edqtg")

# print(finnhub_client.support_resistance('AAPL', 'D'))


# '''
# Get support and resistance levels for a symbol.

# symbol (req): 
# 	stock symbol
# resolution (req):
# 	Supported resolution includes 1, 5, 15, 30, 60, D, W, M.
# 	Some timeframes might not be available depending on the exchange.
# '''
# def get_support_resistance(symbol, timeframe):
# 	return



# SuperFastPython.com
# example of stopping all child processes with kill
from time import sleep
from multiprocessing import Process
from multiprocessing import active_children
 
# function executed in a child process
def task():
    # block for a while
    sleep(10)
 
# protect the entry point
if __name__ == '__main__':
    # start many child processes
    children = [Process(target=task) for _ in range(10)]
    # start all child processes
    for child in children:
        child.start()
    # wait a moment
    print('Main waiting...')
    sleep(2)
    # get all active child processes
    active = active_children()
    print(f'Active Children: {len(active)}')
    # kill all active children
    for child in active:
        child.kill()
    # block until all children have closed
    for child in active:
        child.join()
    # report active children
    active = active_children()
    print(f'Active Children: {len(active)}')