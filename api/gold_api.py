import http.client
import mimetypes

conn = http.client.HTTPSConnection("www.goldapi.io")
payload = ''
headers = {
  'x-access-token': 'goldapi-1gfnskt8qpsd0-io',
  'Content-Type': 'application/json'
}

conn.request("GET", "/api/XAU/USD", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))