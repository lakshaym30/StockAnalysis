import urllib
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# Collect and parse first page

finviz_url = 'https://finviz.com/quote.ashx?t=ADI'
news_tables = {}
url = finviz_url
quote_req = Request(url=url, headers={'user-agent': 'my-app'})
quote_response = urlopen(quote_req)
quote_soup = BeautifulSoup(quote_response, features='html.parser')
news_table = quote_soup.find(id='news-table')
news_tables['ADI'] = news_table

for ticker in news_tables:
    news_links = []
    for row in news_tables[ticker].findAll('tr'):
        title = row.a['href']
        news_links.append([title])
    news_tables[ticker] = news_links


for ticker in news_tables:
    for index in range(len(news_tables[ticker]) - 1):
        news_url = news_tables[ticker][index][0]
        substring = 'www.moodys.com'
        if substring in news_url:
            continue
        news_req = Request(url=news_url, headers={'user-agent': 'my-app'})
        try:
            news_response = urlopen(news_req)
        except urllib.error.HTTPError:
            pass
        news_soup = BeautifulSoup(news_response, features='html.parser')
        article = news_soup.find_all('p')
        final_result = ''
        for i in range(len(article) - 1):
            final_result += article[i].text
        file_name = ticker + '-' + str(index) + '.txt'
        print('writing: ' + file_name)
        f = open(file_name, "a")
        f.write(final_result)
        f.close()





