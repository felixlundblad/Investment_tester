import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import  datetime as dt
import pandas_datareader.data as web


def get_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    return tickers


def get_data_from_yahoo(start_y=2000, start_m=1, start_d=1, end_y=2019, end_m=1, end_d=1, amount_of_tickers=499, reload_sp500=False):
    if reload_sp500:
        tickers = get_sp500_tickers()
    else:
        with open('data/sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('data/stock_dfs'):
        os.makedirs('data/stock_dfs')

    start = dt.datetime(start_y, start_m, start_d)
    end = dt.datetime(end_y, end_m, end_d)

    for i, ticker in enumerate(tickers[:amount_of_tickers]):
        print('Getting ticker number: ', i, '(', ticker, ')')
        if not os.path.exists('data/stock_dfs/' + ticker + '.csv'):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('data/stock_dfs/' + ticker + '.csv')
        else:
            print('Already have', ticker)


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('data/sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers


def main():
    get_data_from_yahoo()


if __name__ == '__main__':
    main()
