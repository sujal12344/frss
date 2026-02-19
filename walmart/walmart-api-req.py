import requests

payload = { 'api_key': 'f3ab67bd2202759f51141d9a79884789', 'product_id': '17702404979' }
r = requests.get('https://api.scraperapi.com/structured/walmart/review/v1', params=payload)
print(r.text)
