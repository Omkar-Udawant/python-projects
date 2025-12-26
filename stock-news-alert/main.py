import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHA_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHA_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json().get("Time Series (Daily)")

if not stock_data:
    print("Stock data unavailable. API limit or invalid key.")
    exit()

data_list = list(stock_data.values())

yesterday_close = float(data_list[0]["4. close"])
day_before_close = float(data_list[1]["4. close"])

difference = abs(yesterday_close - day_before_close)
percentage_change = (difference / day_before_close) * 100

direction = "🔺" if yesterday_close > day_before_close else "🔻"

print(f"{STOCK_NAME}: {direction}{round(percentage_change,1)}%")

if percentage_change >= 5:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json().get("articles", [])[:3]

    formatted_articles = [
        f"{STOCK_NAME}: {direction}{round(percentage_change,1)}%\n"
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in articles
    ]

    for article in formatted_articles:
        print("\n" + article)
else:
    print("No significant stock movement today.")
