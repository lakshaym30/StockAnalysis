import http
import urllib
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# Collect top 100 stock tickers
url = 'https://www.stockmonitor.com/nasdaq-stocks/'
req = Request(url=url, headers={'user-agent': 'my-app'})
response = urlopen(req)
tickers = []
soup = BeautifulSoup(response, features='html.parser')
table = soup.find('table')
table_rows = table.find_all('tr')
for i in range(24, 99):
    td = table_rows[i].findChildren("td", recursive=True)
    for ticker in td:
        tickers.append(td[1].text.strip("\n"))
        break

print(tickers)

#Collect ticker news tables from finviz
finviz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
for ticker in tickers:
    quote_url = finviz_url + ticker
    quote_req = Request(url=quote_url, headers={'user-agent': 'my-app'})
    quote_response = urlopen(quote_req)
    quote_soup = BeautifulSoup(quote_response, features='html.parser')
    news_table = quote_soup.find(id='news-table')
    news_tables[ticker] = news_table
    print(ticker)

# Collect links from news table
for ticker in news_tables:
    news_links = []
    for row in news_tables[ticker].findAll('tr'):
        title = row.a['href']
        news_links.append([title])
        news_tables[ticker] = news_links
    print('done:' + ticker)

# Get text from links
for ticker in news_tables:
    path = '/Users/lakshaymaharana/PycharmProjects/StockAnalysis/' + ticker
    os.mkdir(path)
    os.chdir(path)
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
        try:
            news_soup = BeautifulSoup(news_response, features='html.parser')
        except http.client.IncompleteRead:
            pass
        article = news_soup.find_all('p')
        final_result = ''
        for i in range(len(article) - 1):
            final_result += article[i].text + " "
        file_name = ticker + '-' + str(index) + '.txt'
        parser = PlaintextParser.from_string(str(final_result), Tokenizer('english'))
        stemmer = Stemmer('english')
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words('english')
        print('writing: ' + file_name)
        f = open(file_name, "a")
        for sentence in summarizer(parser.document, 2):
            f.write(str(sentence))
        f.close()













