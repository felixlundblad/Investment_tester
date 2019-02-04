import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import style
import pandas_datareader.data as web
import numpy as np

'''
Useful tags:
^OMX
'''

style.use('ggplot')

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2020, 1, 1)
df = web.DataReader('^OMX', 'yahoo', start, end).drop('Volume', axis=1)


def test_ma(df,
            starting_balance=-1,
            start_pos=200,
            end_pos=len(df),
            moving_average_over=200,
            print_trades=False):
    first_buy_at = 0
    balance = starting_balance
    shares = 0
    sold_last = True
    ma = df['Adj Close'].rolling(window=moving_average_over, min_periods=0).mean()
    if df.iloc[start_pos]['Adj Close'] > ma[start_pos]:
        first_buy_at = df.iloc[start_pos]['Adj Close']
        if print_trades:
            print('First buy at:', first_buy_at)
        if balance == 0:
            shares = 1
        else:
            shares = balance / df.iloc[start_pos]['Adj Close']
        sold_last = False

    hist = pd.DataFrame(0, dtype=float, index=df.index, columns=['Trading History'])

    for i in range(start_pos, end_pos):
        price = df.iloc[i]['Adj Close'] if df.iloc[i]['Adj Close'] != 0 else price
        yesterday_price = df.iloc[i - 1]['Adj Close'] if df.iloc[i - 1]['Adj Close'] != 0 else yesterday_price
        if yesterday_price < price and ma[i] <= price and sold_last:
            if first_buy_at == 0:
                first_buy_at = df.iloc[i]['Adj Close']
                if print_trades:
                    print('First buy at:', first_buy_at)
            sold_last = False
            if balance == -1:
                balance = 0
                shares = 1
            else:
                shares = balance / price
                balance = 0
            if print_trades:
                print('Buy:', df.iloc[i])
        elif yesterday_price > price and ma[i] >= price and balance != -1 and not sold_last:
            sold_last = True
            balance = shares * price
            shares = 0
            if print_trades:
                print('Sell:', balance, df.iloc[i])
        if balance != -1:
            current_worth = balance + shares * price
            hist['Trading History'][i] = current_worth
    if print_trades:
        print(balance)
    return first_buy_at, hist


def test_50ma200(df,
                 starting_balance=-1,
                 start_pos=200,
                 end_pos=len(df),
                 main_average_over=200,
                 crossing_average_over=50,
                 print_trades=False):
    first_buy_at = 0
    balance = starting_balance
    shares = 0
    sold_last = True
    ma_main = df['Adj Close'].rolling(window=main_average_over, min_periods=0).mean()
    ma_cross = df['Adj Close'].rolling(window=crossing_average_over, min_periods=0).mean()
    if ma_cross[start_pos] > ma_main[start_pos]:
        first_buy_at = df.iloc[start_pos]['Adj Close']
        if print_trades:
            print('First buy at:', first_buy_at)
        if balance == 0:
            shares = 1
        else:
            shares = balance / df.iloc[start_pos]['Adj Close']
            balance = 0
        sold_last = False

    hist = pd.DataFrame(0, dtype=float, index=df.index, columns=['Trading History'])

    for i in range(start_pos, end_pos):
        price = df.iloc[i]['Adj Close'] if df.iloc[i]['Adj Close'] != 0 else price
        ma50_today = ma_cross[i]
        ma50_yesterday = ma_cross[i - 1]
        if ma50_yesterday < ma50_today and ma_main[i] <= ma50_today and sold_last:
            if first_buy_at == 0:
                first_buy_at = df.iloc[i]['Adj Close']
                print('First buy at:', first_buy_at)
            sold_last = False
            if balance == -1:
                balance = 0
                shares = 1
            else:
                shares = balance / price
                balance = 0
            if print_trades:
                print('Buy:', df.iloc[i])
        elif ma50_yesterday > ma50_today and ma_main[i] >= ma50_today and balance != -1 and not sold_last:
            sold_last = True
            balance = shares * price
            shares = 0
            if print_trades:
                print('Sell:', balance, df.iloc[i])
        if balance != -1:
            current_worth = balance + shares * price
            hist['Trading History'][i] = current_worth
    if print_trades:
        print(balance)
    return first_buy_at, hist


def test_any_two_crossing(df,
                          ma_main,
                          ma_cross,
                          starting_balance=-1,
                          saving_per_period=0,
                          period_length=0,
                          start_pos=200,
                          end_pos=len(df),
                          print_trades=False):
    short_at = 0
    first_buy_at = 0
    balance = starting_balance
    shares = 0
    sold_last = True
    if ma_cross[start_pos] > ma_main[start_pos]:
        first_buy_at = df.iloc[start_pos]['Adj Close']
        if print_trades:
            print('First buy at:', first_buy_at)
        if balance == -1:
            shares = 1
        else:
            shares = balance / df.iloc[start_pos]['Adj Close']
            balance = 0
        sold_last = False

    hist = pd.DataFrame(0, dtype=float, index=df.index, columns=['Trading History'])

    for i in range(start_pos, end_pos):
        price = df.iloc[i]['Adj Close'] if df.iloc[i]['Adj Close'] != 0 else price
        if period_length != 0:
            if i != 0 and i % period_length == 0:
                if ma_cross[i] < ma_main[i]:
                    balance += saving_per_period
                else:
                    shares += saving_per_period/price
        crossing_today = ma_cross[i]
        crossing_yesterday = ma_cross[i - 1]
        if crossing_yesterday < crossing_today and ma_main[i] <= crossing_today and sold_last:
            if first_buy_at == 0:
                first_buy_at = df.iloc[i]['Adj Close']
                if print_trades:
                    print('First buy at:', first_buy_at)
            sold_last = False
            if balance == -1:
                balance = 0
                shares = 1
            else:
                balance += -shares * (short_at - price)
                shares = balance / price
                balance = 0
            if print_trades:
                print('Buy:', df.iloc[i])
        elif crossing_yesterday > crossing_today and ma_main[i] >= crossing_today and balance != -1 and not sold_last:
            sold_last = True
            balance = shares * price
            short_at = price
            shares = -shares
            if print_trades:
                print('Sell:', balance, df.iloc[i])
        if balance != -1:
            current_worth = balance + shares * price if not sold_last else balance - shares * (short_at - price)
            hist['Trading History'][i] = current_worth
    if print_trades:
        print(balance)
    return first_buy_at, hist


def test_buy_hold(df,
                  starting_balance=0,
                  saving_per_period=0,
                  period_length=0,
                  start_pos=200,
                  end_pos=len(df)):
    hist = pd.DataFrame(0, dtype=float, index=df.index, columns=['Trading History'])
    first_buy_at = df['Adj Close'].iloc[start_pos]
    shares = starting_balance / first_buy_at

    for i in range(start_pos, end_pos):
        price = df.iloc[i]['Adj Close']
        current_worth = shares * price
        hist['Trading History'][i] = current_worth
        if i != 0 and i % period_length == 0:
            shares += saving_per_period / price

    return first_buy_at, hist


def calc_buy_hold_annual_growth(df, start_pos=200, dec=3):
    years = (int(str(df.last_valid_index()).split('-')[0]) - int(str(df.index[start_pos]).split('-')[0]))
    start_sum = df['Adj Close'].iloc[start_pos]
    end_sum = df['Adj Close'][-1]
    return round(100 * (end_sum / start_sum) ** (1 / years) - 100, dec)


def calc_model_annual_growth(df, tag='Trading History', dec=3):
    years = (int(str(df.last_valid_index()).split('-')[0]) - int(str(df.index[start_pos]).split('-')[0]))
    start_sum = df[tag].iloc[df[tag].nonzero()[0][0]]
    end_sum = df[tag][-1]
    return round(100 * (end_sum / start_sum) ** (1 / years) - 100, dec)


def list_all_annual_growth(df, tags, dec=3):
    return [(tag.replace('Trading History ', ''),
             round(calc_model_annual_growth(df, tag), dec)) for tag in tags]


def print_all_annual_growth(df, tags, dec=3):
    [print(tag.replace('Trading History ', '') + ':\t',
           round(calc_model_annual_growth(df, tag), dec), '% per year') for tag in tags]


def print_top_list(df, org_list, length=0):
    print('\n' + 'Full ranking list:') if length == 0 else print('\n' + 'Top ' + str(length) + ':')
    top_list = list_all_annual_growth(df, org_list)
    top_list.sort(key=lambda tup: tup[1], reverse=True)
    [print(l[0] + ':\t', l[1], '% per year') for l in (top_list if length == 0 else top_list[:length])]


def test_multiple_two_sma_crossing(df,
                                   plotting_list,
                                   first_buy_at=-1,
                                   start_crossing=50,
                                   end_crossing=51,
                                   interval_crossing=10,
                                   start_main=200,
                                   end_main=201,
                                   interval_main=10,
                                   print_performance=False):
    for main in range(start_main, end_main, interval_main):
        for crossing in range(start_crossing, end_crossing, interval_crossing):
            plotting_list.append('Trading History SMA' + str(crossing) + '/' + str(main))
            _, df['Trading History SMA' + str(crossing) + '/' + str(main)] = \
                test_any_two_crossing(df,
                                      df['Adj Close'].rolling(window=main,
                                                              min_periods=0).mean(),
                                      df['Adj Close'].rolling(window=crossing,
                                                              min_periods=0).mean(),
                                      starting_balance=first_buy_at,
                                      start_pos=start_pos, end_pos=end_pos)
            if print_performance:
                print('SMA' + str(crossing) + '/' + str(main) + ' model performance:',
                      calc_model_annual_growth(df, 'Trading History SMA' + str(crossing) + '/' + str(main)))


def test_multiple_two_ema_crossing(df,
                                   plotting_list,
                                   first_buy_at=-1,
                                   start_crossing=50,
                                   end_crossing=51,
                                   interval_crossing=10,
                                   start_main=200,
                                   end_main=201,
                                   interval_main=10,
                                   print_performance=False,
                                   print_loading_bar=True):
    total_tasks = ((end_main - start_main)//interval_main) * ((end_crossing - start_crossing)//interval_crossing)
    counter = 0
    for main in range(start_main, end_main, interval_main):
        for crossing in range(start_crossing, end_crossing, interval_crossing):
            if print_loading_bar:
                print(str(counter) + '/' + str(total_tasks))
            plotting_list.append('Trading History EMA' + str(crossing) + '/' + str(main))
            _, df['Trading History EMA' + str(crossing) + '/' + str(main)] = \
                test_any_two_crossing(df,
                                      df['Adj Close'].rolling(window=main,
                                                              min_periods=0).mean(),
                                      df['Adj Close'].ewm(span=crossing,
                                                          min_periods=0).mean(),
                                      starting_balance=first_buy_at,
                                      start_pos=start_pos, end_pos=end_pos)
            if print_performance:
                print('EMA' + str(crossing) + '/' + str(main) + ' model performance:',
                      calc_model_annual_growth(df, 'Trading History EMA' + str(crossing) + '/' + str(main)))


start_pos = 200
end_pos = len(df['Adj Close'])
print('Buy hold:\t', calc_buy_hold_annual_growth(df, start_pos), '% per year')
plotting_list = ['Adj Close', 'SMA200', 'SMA50', 'EMA50']
non_trading_plots = len(plotting_list)

df['SMA200'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
df['SMA50'] = df['Adj Close'].rolling(window=50, min_periods=0).mean()
df['EMA50'] = df['Adj Close'].ewm(span=50, min_periods=0).mean()

first_buy_at, df['Trading History SMA200'] = test_ma(df, start_pos=start_pos, end_pos=end_pos, print_trades=False)
print('SMA200:\t\t', calc_model_annual_growth(df, 'Trading History SMA200'), '% per year')

plotting_list.extend(['Trading History EMA50/200', 'Trading History SMA50/200', 'Accumulate Buy Hold'])

_, df['Trading History EMA50/200'] = test_any_two_crossing(df,
                                                           df['Adj Close'].rolling(window=200,
                                                                                   min_periods=0).mean(),
                                                           df['Adj Close'].ewm(span=60, min_periods=0).mean(), starting_balance=10000, saving_per_period=10000, period_length=21)

_, df['Trading History SMA50/200'] = test_any_two_crossing(df,
                                                           df['Adj Close'].rolling(window=200,
                                                                                   min_periods=0).mean(),
                                                           df['Adj Close'].rolling(window=70, min_periods=0).mean(), starting_balance=10000, saving_per_period=10000, period_length=21)

_, df['Accumulate Buy Hold'] = test_buy_hold(df, starting_balance=10000, saving_per_period=10000, period_length=21)

# test_multiple_two_ema_crossing(df, plotting_list, first_buy_at, 30, 51, 10, 200, 201, 10)
# test_multiple_two_sma_crossing(df, plotting_list, first_buy_at, 30, 71, 10, 200, 260, 10)

print_top_list(df, plotting_list[non_trading_plots:])

df[plotting_list].plot()
plt.show()
