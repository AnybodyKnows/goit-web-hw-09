import re
import json
from datetime import datetime
import lxml
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com/'


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_author_inf(url):
    soup = get_soup(url)
    name = soup.select_one(".author-title").text
    birth_date = soup.select_one(".author-born-date").text
    birth_place = soup.select_one(".author-born-location").text
    description = soup.select_one(".author-description").text

    return {
        "fullname": name,
        "born_date": birth_date,
        "born_location": birth_place,
        "description": description.strip()
    }


def scrape_quotes():
    quotes = []
    authors_info = []
    page = 1
    while True:
        soup = get_soup(f"{BASE_URL}/page/{page}/")
        quote_elements = soup.select(".quote")

        if not quote_elements:
            break

        for quote_element in quote_elements:
            quote = quote_element.select_one(".text").text
            author = quote_element.select_one(".author").text
            author_url = quote_element.select_one("span > a")["href"]
            tags = quote_element.select(".tag")
            tags = [tag.text for tag in tags]
            quote_info = {
                "tags": tags,
                "author": author,
                "quote": quote.strip()
            }
            quotes.append(quote_info)
            author = get_author_inf(f"{BASE_URL}{author_url}")
            authors_info.append(author)
        page += 1
    return quotes, authors_info


def save_quotes(data, filename):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    quotes, authors = scrape_quotes()

    save_quotes(quotes, "quotes.json")
    save_quotes(authors, "authors.json")



