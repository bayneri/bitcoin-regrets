import datetime
import urllib2
import requests
import json
from random import randrange
from datetime import timedelta
import math

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def random_investment():
    return randrange(30, 1000)

initial_bitcoin_date = datetime.datetime.strptime('2010-07-18', '%Y-%m-%d').date()
end_date = datetime.datetime.now().date()

current_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
current_res = requests.get(current_url)
current_rate = json.loads(current_res.content)['bpi']['USD']['rate_float']

#find an investment date which would cause regret
while True:
    investment_date = random_date(initial_bitcoin_date,end_date).strftime('%Y-%m-%d')
    investment_amount = random_investment()
    investment_url = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=%s&end=%s' %(investment_date, investment_date)
    investment_res = requests.get(investment_url)
    investment_rate = json.loads(investment_res.content)['bpi'][investment_date]
    if investment_rate < current_rate:
        break

value = int((current_rate/investment_rate) * investment_amount)

current_amount = "{:,}".format(value)

print(investment_date)
print(investment_amount)
print(current_amount)