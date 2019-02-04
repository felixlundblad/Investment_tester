import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import style
import pandas_datareader.data as web
import numpy as np

'''
Useful tags:
^OMXSPI
^OMX
'''


class Stock_tester:
    def __init__(self,
                 ticker='^OMX',
                 start=dt.datetime(2000, 1, 1),
                 end=dt.datetime(2020, 1, 1),
                 ):
        self.ticker = ticker
        self.start = start
        self.end = end
        style.use('ggplot')
        self.df = web.DataReader(ticker, 'yahoo', self.start, self.end).drop('Volume', axis=1)

    def test_ma(self,
                starting_balance=-1,
                start_pos=200,
                end_pos=0,
                moving_average_over=200,
                print_trades=False):
        if end_pos == 0:
            end_pos = len(self.df)
        first_buy_at = 0
        balance = starting_balance
        shares = 0
        sold_last = True
        ma = self.df['Adj Close'].rolling(window=moving_average_over, min_periods=0).mean()
        if self.df.iloc[start_pos]['Adj Close'] > ma[start_pos]:
            first_buy_at = self.df.iloc[start_pos]['Adj Close']
            if print_trades:
                print('First buy at:', first_buy_at)
            if balance == 0:
                shares = 1
            else:
                shares = balance / self.df.iloc[start_pos]['Adj Close']
            sold_last = False

        hist = pd.DataFrame(0, dtype=float, index=self.df.index, columns=['Trading History'])

        for i in range(start_pos, end_pos):
            price = self.df.iloc[i]['Adj Close'] if self.df.iloc[i]['Adj Close'] != 0 else price
            yesterday_price = self.df.iloc[i - 1]['Adj Close'] if self.df.iloc[i - 1][
                                                                      'Adj Close'] != 0 else yesterday_price
            if yesterday_price < price and ma[i] <= price and sold_last:
                if first_buy_at == 0:
                    first_buy_at = self.df.iloc[i]['Adj Close']
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
                    print('Buy:', self.df.iloc[i])
            elif yesterday_price > price and ma[i] >= price and balance != -1 and not sold_last:
                sold_last = True
                balance = shares * price
                shares = 0
                if print_trades:
                    print('Sell:', balance, self.df.iloc[i])
            if balance != -1:
                current_worth = balance + shares * price
                hist['Trading History'][i] = current_worth
        if print_trades:
            print(balance)
        return first_buy_at, hist

    def test_50ma200(self,
                     starting_balance=-1,
                     start_pos=200,
                     end_pos=0,
                     main_average_over=200,
                     crossing_average_over=50,
                     print_trades=False):
        if end_pos == 0:
            end_pos = len(self.df)
        first_buy_at = 0
        balance = starting_balance
        shares = 0
        sold_last = True
        ma_main = self.df['Adj Close'].rolling(window=main_average_over, min_periods=0).mean()
        ma_cross = self.df['Adj Close'].rolling(window=crossing_average_over, min_periods=0).mean()
        if ma_cross[start_pos] > ma_main[start_pos]:
            first_buy_at = self.df.iloc[start_pos]['Adj Close']
            if print_trades:
                print('First buy at:', first_buy_at)
            if balance == 0:
                shares = 1
            else:
                shares = balance / self.df.iloc[start_pos]['Adj Close']
                balance = 0
            sold_last = False

        hist = pd.DataFrame(0, dtype=float, index=self.df.index, columns=['Trading History'])

        for i in range(start_pos, end_pos):
            price = self.df.iloc[i]['Adj Close'] if self.df.iloc[i]['Adj Close'] != 0 else price
            ma50_today = ma_cross[i]
            ma50_yesterday = ma_cross[i - 1]
            if ma50_yesterday < ma50_today and ma_main[i] <= ma50_today and sold_last:
                if first_buy_at == 0:
                    first_buy_at = self.df.iloc[i]['Adj Close']
                    print('First buy at:', first_buy_at)
                sold_last = False
                if balance == -1:
                    balance = 0
                    shares = 1
                else:
                    shares = balance / price
                    balance = 0
                if print_trades:
                    print('Buy:', self.df.iloc[i])
            elif ma50_yesterday > ma50_today and ma_main[i] >= ma50_today and balance != -1 and not sold_last:
                sold_last = True
                balance = shares * price
                shares = 0
                if print_trades:
                    print('Sell:', balance, self.df.iloc[i])
            if balance != -1:
                current_worth = balance + shares * price
                hist['Trading History'][i] = current_worth
        if print_trades:
            print(balance)
        return first_buy_at, hist

    def test_any_two_crossing(self,
                              ma_main,
                              ma_cross,
                              starting_balance=-1,
                              start_pos=200,
                              end_pos=0,
                              print_trades=False):
        if end_pos == 0:
            end_pos = len(self.df)
        first_buy_at = 0
        balance = starting_balance
        shares = 0
        sold_last = True
        if ma_cross[start_pos] > ma_main[start_pos]:
            first_buy_at = self.df.iloc[start_pos]['Adj Close']
            if print_trades:
                print('First buy at:', first_buy_at)
            if balance == -1:
                shares = 1
            else:
                shares = balance / self.df.iloc[start_pos]['Adj Close']
                balance = 0
            sold_last = False

        hist = pd.DataFrame(0, dtype=float, index=self.df.index, columns=['Trading History'])

        for i in range(start_pos, end_pos):
            price = self.df.iloc[i]['Adj Close'] if self.df.iloc[i]['Adj Close'] != 0 else price
            crossing_today = ma_cross[i]
            crossing_yesterday = ma_cross[i - 1]
            if crossing_yesterday < crossing_today and ma_main[i] <= crossing_today and sold_last:
                if first_buy_at == 0:
                    first_buy_at = self.df.iloc[i]['Adj Close']
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
                    print('Buy:', self.df.iloc[i])
            elif crossing_yesterday > crossing_today and ma_main[
                i] >= crossing_today and balance != -1 and not sold_last:
                sold_last = True
                balance = shares * price
                shares = 0
                if print_trades:
                    print('Sell:', balance, self.df.iloc[i])
            if balance != -1:
                current_worth = balance + shares * price
                hist['Trading History'][i] = current_worth
        if print_trades:
            print(balance)
        return first_buy_at, hist

    def calc_buy_hold_annual_growth(self, start_pos=200, dec=3):
        years = (int(str(self.df.last_valid_index()).split('-')[0]) - int(str(self.df.index[start_pos]).split('-')[0]))
        start_sum = self.df['Adj Close'].iloc[start_pos]
        end_sum = self.df['Adj Close'][-1]
        return round(100 * (end_sum / start_sum) ** (1 / years) - 100, dec)

    def calc_model_annual_growth(self, tag='Trading History', dec=3):
        years = (int(str(self.df.last_valid_index()).split('-')[0]) - int(str(self.df.index[self.start]).split('-')[0]))
        start_sum = self.df[tag].iloc[self.df[tag].nonzero()[0][0]]
        end_sum = self.df[tag][-1]
        return round(100 * (end_sum / start_sum) ** (1 / years) - 100, dec)

    def list_all_annual_growth(self, tags, dec=3):
        return [(tag.replace('Trading History ', ''),
                 round(self.calc_model_annual_growth(self.df, tag), dec)) for tag in tags]

    def print_all_annual_growth(self, tags, dec=3):
        [print(tag.replace('Trading History ', '') + ':\t',
               round(self.calc_model_annual_growth(self.df, tag), dec), '% per year') for tag in tags]

    def print_top_list(self, org_list, length=0):
        print('\n' + 'Full ranking list:') if length == 0 else print('\n' + 'Top ' + str(length) + ':')
        top_list = self.list_all_annual_growth(self.df, org_list)
        top_list.sort(key=lambda tup: tup[1], reverse=True)
        [print(l[0] + ':\t', l[1], '% per year') for l in (top_list if length == 0 else top_list[:length])]

    def test_multiple_two_sma_crossing(self,
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
                _, self.df['Trading History SMA' + str(crossing) + '/' + str(main)] = \
                    self.test_any_two_crossing(self.df,
                                          self.df['Adj Close'].rolling(window=main,
                                                                       min_periods=0).mean(),
                                          self.df['Adj Close'].rolling(window=crossing,
                                                                       min_periods=0).mean(),
                                          starting_balance=first_buy_at,
                                          start_pos=self.start, end_pos=self.end)
                if print_performance:
                    print('SMA' + str(crossing) + '/' + str(main) + ' model performance:',
                          self.calc_model_annual_growth(self.df, 'Trading History SMA' + str(crossing) + '/' + str(main)))

    def test_multiple_two_ema_crossing(self,
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
                plotting_list.append('Trading History EMA' + str(crossing) + '/' + str(main))
                _, self.df['Trading History EMA' + str(crossing) + '/' + str(main)] = \
                    self.test_any_two_crossing(self.df,
                                          self.df['Adj Close'].rolling(window=main,
                                                                       min_periods=0).mean(),
                                          self.df['Adj Close'].ewm(span=crossing,
                                                                   min_periods=0).mean(),
                                          starting_balance=first_buy_at,
                                          start_pos=self.start, end_pos=self.end)
                if print_performance:
                    print('EMA' + str(crossing) + '/' + str(main) + ' model performance:',
                          self.calc_model_annual_growth(self.df, 'Trading History EMA' + str(crossing) + '/' + str(main)))

    def get_df(self):
        return self.df

    def make_sma(self, window=200):
        return self.df['Adj Close'].rolling(window=window, min_periods=0).mean()

    def make_ema(self, span=50):
        return self.df['Adj Close'].ewm(span=50, min_periods=0).mean()


def main():
    s = Stock_tester()
    start_pos = 200
    end_pos = len(s.df['Adj Close'])
    print('Buy hold:\t', s.calc_buy_hold_annual_growth(s.df, start_pos), '% per year')
    plotting_list = ['Adj Close', 'SMA200', 'SMA50', 'EMA50']
    non_trading_plots = len(plotting_list)

    s.df['SMA200'] = s.df['Adj Close'].rolling(window=200, min_periods=0).mean()
    s.df['SMA50'] = s.df['Adj Close'].rolling(window=50, min_periods=0).mean()
    s.df['EMA50'] = s.df['Adj Close'].ewm(span=50, min_periods=0).mean()

    first_buy_at, s.df['Trading History SMA200'] = s.test_ma(s.df, start_pos=start_pos, end_pos=end_pos,
                                                              print_trades=False)
    print('SMA200:\t\t', s.calc_model_annual_growth(s.df, 'Trading History SMA200'), '% per year')

    plotting_list.extend(['Trading History EMA50/200', 'Trading History SMA50/200'])

    _, s.df['Trading History EMA50/200'] = s.test_any_two_crossing(s.df,
                                                                    s.df['Adj Close'].rolling(window=200,
                                                                                                 min_periods=0).mean(),
                                                                    s.df['Adj Close'].ewm(span=60,
                                                                                             min_periods=0).mean())

    _, s.df['Trading History SMA50/200'] = s.test_any_two_crossing(s.df,
                                                                    s.df['Adj Close'].rolling(window=200,
                                                                                                 min_periods=0).mean(),
                                                                    s.df['Adj Close'].rolling(window=70,
                                                                                                 min_periods=0).mean())

    s.test_multiple_two_ema_crossing(s.df, plotting_list, first_buy_at, 30, 71, 10, 200, 260, 10)
    s.test_multiple_two_sma_crossing(s.df, plotting_list, first_buy_at, 30, 71, 10, 200, 260, 10)

    s.print_top_list(s.df, plotting_list[non_trading_plots:], 10)

    s.df[plotting_list].plot()
    plt.show()


if __name__ == '__main__':
    main()
