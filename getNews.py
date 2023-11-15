import json
import os
from http import HTTPStatus

import requests

open_news_api_key = os.environ["TOKEN_NEWSAPI"]


def parse_search_news(response: json):
    news_info = []
    for article in response["articles"]:
        news_info.append(article["title"])
    return json.dumps(news_info)


def search_news(keyword: str):
    headers = {"X-Api-Key": open_news_api_key}

    url = "https://newsapi.org/v2/everything"

    params = {"q": keyword, "sortBy": "popularity", "pageSize": 5}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == HTTPStatus.OK:
        data = response.json()
    return parse_search_news(data)


def fetch_headlines(category: str):
    headers = {"X-Api-Key": open_news_api_key}

    url = "https://newsapi.org/v2/top-headlines"

    params = {"country": "jp", "category": category, "pageSize": 5}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == HTTPStatus.OK:
        data = response.json()
    return parse_search_news(data)


if __name__ == "__main__":
    print(search_news("名古屋"))
