
API_KEY= '6136bd6b643853.28888131'


BASE_URL='https://eodhistoricaldata.com/api/eod'


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time



'''
"5m"
"yearly""monthly""weekly""daily""hourly""5m""10m""15m""30m""45m""1h""2h""3h""4h""6h""12h""24h""1d""2d""3d""7d""14d""15d""30d""60d""90d""365d"
'''
def get_historical_quotes(symbol, exchange, start_timestamp, end_timestamp):
    req_url = BASE_URL + '/' + symbol + '.' + exchange
    parameters = {
        'api_token': API_KEY,
        'symbol': symbol,
        'time_start': start_timestamp,
        'time_end': end_timestamp,
        'fmt': 'json'
    }
    headers = {
        'Accepts': 'application/json',
        # 'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(req_url, params=parameters)
        data = json.loads(response.text)
        print(data)
        historical_quotes = data

        return historical_quotes

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def get_current_timestamp():
    return time.time()


print(get_historical_quotes('DXY', 'INDX', get_current_timestamp()-(86400 * 365 * 20), get_current_timestamp()))
# print(get_historical_quotes('GOLD', 'US', get_current_timestamp()-(86400 * 365 * 20), get_current_timestamp()))
