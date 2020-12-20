import requests
import time
from newsapi import NewsApiClient
from twilio.rest import Client
import os

def percentage_change(base_value : float, changed_value : float):
    """ function returning % change of inserted values"""
    increase = ((changed_value/base_value)*100)-100
    return increase

def get_news(day):
    """Function taking yesterday date then returning 3 news sorted by popularity in dic format with keys: title, description"""
    parameters_news = {
        "q": "bitcoin",
        "from": day,
        "sortBy": "popularity",
        "apiKey": API_KEY_NEWS,
        "language": "en",
        }
    messages = {
        "title":[],
        "description": [],
    }

    response_news = requests.get("http://newsapi.org/v2/everything" , params=parameters_news)
    response_news.raise_for_status()

    news_data = response_news.json()
    articles = news_data["articles"]

    for i in range(0, 3):
        ran = articles[i]
        messages["title"].append(ran['title'])
        messages["description"].append(ran['description'])

    return messages
    


#--------------------------------- CONSTANTS --------------------------------


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

API_NUMBER = os.environ.get("API_NUMBER")
RECIEVER_NUMBER = os.environ.get("RECIEVER_NUMBER")

CRYPTO_CURRENCY = "BTC"
FIAT_CURRENCY = "USD"
FUNCTION = "DIGITAL_CURRENCY_DAILY"
API_KEY_STOCK = os.environ.get("API_KEY_STOCK")
API_KEY_NEWS = os.environ.get("API_KEY_NEWS")


#--------------------------------- TAKING PRICE DATA --------------------------------
parameters = {
    "function":FUNCTION,
    "symbol": CRYPTO_CURRENCY,
    "market": FIAT_CURRENCY,
    "apikey": API_KEY_STOCK,
}
response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
currency_data = response.json()


# Creating Yesterday date data as year-month-day format
yesterday = (time.strftime("%Y,%m,%d")).split(",")
yest = int(yesterday[2]) - 1
yesterday[2] = str(yest)
yest_data = "-".join(yesterday)

# Fetching higher and lower exchange value data for yesterday
yesterday_currency_exchange_data = currency_data["Time Series (Digital Currency Daily)"][yest_data]
higher_yesterday = yesterday_currency_exchange_data['2a. high (USD)']
lower_yesterday = yesterday_currency_exchange_data['3a. low (USD)']

# Creating today date data as year-month-day format
day_before_yesterday = (time.strftime("%Y,%m,%d")).split(",")
before = int(day_before_yesterday[2]) - 10
day_before_yesterday[2] = str(before)
day_before_yest_data = "-".join(day_before_yesterday)

# Fetching higher and lower exchange value data for today
day_before_yesterday_currency_exchange_data = currency_data["Time Series (Digital Currency Daily)"][day_before_yest_data]
higher_day_before_yesterday = day_before_yesterday_currency_exchange_data['2a. high (USD)']
lower_day_before_yesterday = day_before_yesterday_currency_exchange_data['3a. low (USD)']


#--------------------------------- Checking price value. is it increasing or decreasing? --------------------------------

if higher_day_before_yesterday < higher_yesterday:
    change = percentage_change(float(higher_day_before_yesterday), float(higher_yesterday))
    change_formated = round(change, 2)
    change_string = f"🔺{change_formated}%"
elif lower_day_before_yesterday > lower_yesterday:
    change = percentage_change(float(lower_day_before_yesterday), float(lower_yesterday))
    change_formated = round(change, 2)
    change_string = f"🔻{change_formated}%"

message_body = get_news(day_before_yest_data)



#--------------------------------- Sending message if change is >= 5% --------------------------------
if change_formated >= 5:
    message_body = get_news(day_before_yest_data)
    body_title = message_body["title"]
    body_description = message_body["description"]
    for k in range(0,3):
        
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages \
                .create(
                    body=f"\n{change_string}\nTitle: {body_title[k]}\nDescription:{body_description[k]}",
                    from_=API_NUMBER,
                    to=RECIEVER_NUMBER,
                )
        print(message.status)
