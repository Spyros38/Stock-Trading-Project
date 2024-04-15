import requests
import os
from dotenv import find_dotenv,load_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

article_list = []
STOCK = "TSLA"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMETERS = {"function": "TIME_SERIES_DAILY",
                    "symbol": STOCK,
                    "apikey": STOCK_API_KEY,
                    }
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_PARAMETERS = {"q": STOCK,
                   "apiKey": NEWS_API_KEY,
                   "sortBy": "relevancy"
                   }


r = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
data = r.json()["Time Series (Daily)"]
print(data)


# # To get yesterday's stock price:
# # Instead of trying to get the last available day - data, we can turn the dictionary into a list
# # So the latest entry is at position 0, as yesterday and at 1 is the day before yesterday.
data_list = [value for (key,value) in data.items()]
yestarday_data = data_list[0]
print(yestarday_data)
yestarday_closing_price = float(yestarday_data["4. close"])

# # To access: yesterday_closing_price = data["Time Series (Daily)"]["2024-02-16"]["4. close"]

# # To get day before yesterdays price:
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

price_difference = abs(yestarday_closing_price - day_before_yesterday_closing_price)

price_difference_percent = round((price_difference / yestarday_closing_price) * 100, 2)

print(price_difference_percent)


if price_difference_percent > 1:
    r2 = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    # # The articles are in a list, so we can use list indexes
    news_data = r2.json()["articles"][:3]
    print(news_data)

    def top_3_articles():
        global article_list
        for article in range(3):
            article_test =f"Brief:{article + 1}\n" + f"Headline: {news_data[article]['title']}\n"
            print(f"Brief:{article}\n")
            print(f"Headline: {news_data[article]['title']}\n")
            print(f"Publishing Date: {news_data[article]['publishedAt']}\n")
            print(f"Brief: {news_data[article]['description']}\n")
            article_list.append(article_test)
        print(article_list)
    top_3_articles()


def telegram_bot_sendtext(bot_message):
    # # Bot token is available on bot father
    # # Remember to hide this
    bot_token = os.getenv("bot_token")
    bot_chatID = os.getenv("bot_chatID")
    telegram_msg_endpoint_url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    telegram_parameters = {"chat_id": bot_chatID,
                           "parse_mode": "Markdown",
                           "text": bot_message}
    response = requests.get(telegram_msg_endpoint_url, params=telegram_parameters)
    response.close()

    return response.json()


if price_difference_percent > 1:
    notification_price = telegram_bot_sendtext(price_difference_percent)
    for item in article_list:
        notification = telegram_bot_sendtext(item)
        print(notification)

