import requests
import pandas as pd
import datetime as dt


def get_data(ticker: str = '.INX') -> pd:
    api_key = ''
    with open('APIKey.txt') as f:
        api_key = f.read()
    '''
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +
                     '&outputsize=full&apikey=' + api_key)
    df = pd.DataFrame([result['Time Series (Daily)'][key] for key in result['Time Series (Daily)'].keys()]).drop(
        ['5. volume'], axis=1)
    '''
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker +
                     '&outputsize=full&apikey=' + api_key)
    result = r.json()

    #[[print(int(key.split('-')[0]), int(key.split('-')[1]), int(key.split('-')[2]))]
    # for key in result['Time Series (Daily)'].keys()]

    df = pd.DataFrame([result['Time Series (Daily)'][key] for key in result['Time Series (Daily)'].keys()])

    #df = pd.DataFrame([result['Time Series (Daily)'][dt.date(int(key.split('-')[0]), int(key.split('-')[1]), int(key.split('-')[2]))]
    #                  for key in result['Time Series (Daily)'].keys()])

    df.index = pd.to_datetime([key for key in result['Time Series (Daily)'].keys()])
    return df.reindex(index=df.index[::-1])
