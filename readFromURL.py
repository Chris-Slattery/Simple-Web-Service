import requests

x = requests.get('http://kylegoslin1.pythonanywhere.com/').json()

#parsed JSON content
forecast = x['forecast']
print(forecast)