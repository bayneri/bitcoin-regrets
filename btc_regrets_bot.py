import datetime
import requests
import json
from random import randrange
from datetime import timedelta
import tweepy

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def random_investment():
    return randrange(30, 1000) # generates a random investment between $30 and $1000

initial_bitcoin_date = datetime.datetime.strptime('2010-07-18', '%Y-%m-%d').date()
end_date = datetime.datetime.now().date()

current_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
current_res = requests.get(current_url)
current_rate = json.loads(current_res.content.decode('UTF-8'))['bpi']['USD']['rate_float']

#find an investment date which would cause regret
while True:
    investment_date_obj = random_date(initial_bitcoin_date,end_date)
    investment_date = investment_date_obj.strftime('%Y-%m-%d')
    investment_amount = random_investment()
    investment_url = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=%s&end=%s' %(investment_date, investment_date)
    investment_res = requests.get(investment_url)
    investment_rate = json.loads(investment_res.content.decode('UTF-8'))['bpi'][investment_date]
    if investment_rate < current_rate:
        break

float_current_amount = int((current_rate/investment_rate) * investment_amount)

current_amount = "{:,}".format(float_current_amount)

CONSUMER_KEY = '***'
CONSUMER_SECRET = '***'
ACCESS_TOKEN = '***'
ACCESS_TOKEN_SECRET = '***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

today_str = end_date.strftime('%b %d, %Y')
investment_date_str = investment_date_obj.strftime('%b %d, %Y')

twit = 'If you had invested $%d on %s; you\'d have $%s today. #BitcoinRegrets' %(investment_amount, investment_date_str, current_amount)

api.update_status(twit)