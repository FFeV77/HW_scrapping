from pprint import pprint
import requests
from bs4 import BeautifulSoup

URL = 'https://habr.com'
KEYWORDS = ['биткоин']
HEADERS = {...}

def matches(hubs, header, body, time, href):
    '''Поиск совпадений с ключевыми словами (KEYWORDS)'''
    for keyword in KEYWORDS:
        if (keyword in hubs) or (header.find(keyword) != -1) or (body.find(keyword) != -1):
            print(f'{time} - {header} - {URL + href}')
    return


def page_soup(page_link):
    base_url = URL + page_link
    data = requests.get(base_url, headers=HEADERS)
    page = data.text
    soup = BeautifulSoup(page, "html5lib")
    return soup


def scrap_main(articles):
    for article in articles:
        header = article.h2.text
        href = article.h2.a['href']
        time = article.time['datetime']
        body = article.find('div', class_ = 'tm-article-body tm-article-snippet__lead').text
        hubs = article.find_all(class_ = 'tm-article-snippet__hubs-item')
        hubs = [hub.text.strip() for hub in hubs]
        matches(hubs, header, body, time, href)
    return


def scrap_article(articles):
    for article in articles:
        href = article.h2.a['href']
        soup = page_soup(href)

        header = soup.find('article').h1.text
        time = soup.find('article').time['datetime']
        hubs = soup.find_all(class_ = 'tm-separated-list__item')
        hubs = [hub.text.strip() for hub in hubs]
        body = soup.find('div', class_ = 'tm-article-body').text
        matches(hubs, header, body, time, href)
    return

if __name__ == '__main__':
    main_page = '/ru/all/'
    soup = page_soup(main_page)
    articles = soup.find_all('article')
    # scrap_main(articles)
    scrap_article(articles)