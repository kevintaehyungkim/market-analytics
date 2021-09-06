
API_KEY= '028e66a4-18bc-4407-b9a5-b9e3c35793db'


BASE_URL='https://pro-api.coinmarketcap.com'
LATEST_QUOTE='/v1/cryptocurrency/quotes/latest'
HISTORICAL_QUOTE='/v1/cryptocurrency/quotes/historical'


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time



def get_latest_quote(symbol):
    req_url = BASE_URL + LATEST_QUOTE
    parameters = {
      'symbol': symbol,
      'convert': 'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(req_url, params=parameters)
      data = json.loads(response.text)
      current_quote = data['data']['BTC']['quote']

      return current_quote

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)



'''
"5m"
"yearly""monthly""weekly""daily""hourly""5m""10m""15m""30m""45m""1h""2h""3h""4h""6h""12h""24h""1d""2d""3d""7d""14d""15d""30d""60d""90d""365d"
'''
def get_historical_quotes(symbol, interval, start_timestamp, end_timestamp):
    req_url = BASE_URL + HISTORICAL_QUOTE
    parameters = {
        'symbol': symbol,
        'interval': interval,
        'time_start': start_timestamp,
        'time_end': end_timestamp,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(req_url, params=parameters)
        data = json.loads(response.text)
        print(data)
        historical_quotes = data['data']['BTC']['quotes']

        return historical_quotes

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def get_current_timestamp():
    return time.time()


# print(get_latest_quote('BTC'))
print(get_historical_quotes('BTC', 'hourly', get_current_timestamp()-86400, get_current_timestamp()))
