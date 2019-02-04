from Bank_account import BankAccount
from Alpha_vantage import get_data

df = get_data('AAPL')
print(df.head(1)['5. adjusted close'])
print(df.tail(1)['5. adjusted close'])

adj_close_prices = df['5. adjusted close'].astype(float).tolist()
print('Amount of days to analyze', len(adj_close_prices))
print()


def test_ma(start_pos=200, end_pos=len(adj_close_prices), moving_average_over=200, starting_balance=1000000, print_hist=False):
    ba = BankAccount(starting_balance)
    ma = df['5. adjusted close'].rolling(window=moving_average_over, min_periods=0).mean().tolist()
    if adj_close_prices[start_pos] > ma[start_pos]:
        #print('BUY')
        ba.open_long('SP500', ba.check_balance() // adj_close_prices[start_pos], adj_close_prices[start_pos])

    for i in range(start_pos, end_pos):
        #print(i, adj_close_prices[i], '\t', ma[i])
        if adj_close_prices[i - 1] < ma[i] and adj_close_prices[i] > ma[i]:
            #print('BUY at', adj_close_prices[i])
            ba.open_long('SP500', ba.check_balance()//adj_close_prices[i], adj_close_prices[i])
        elif adj_close_prices[i - 1] > ma[i] and adj_close_prices[i] < ma[i]:
            #print('SELL at', adj_close_prices[i])
            ba.close_long('SP500', ba.check_holdings('SP500'), adj_close_prices[i])
    if print_hist:
        print(ba.check_history())
    ba.close_long('SP500', ba.check_holdings('SP500'), adj_close_prices[end_pos-1])
    return ba.check_balance()


def test_buy_hold(start_pos=200, end_pos=len(adj_close_prices), starting_balance=1000000, print_hist=False):
    ba = BankAccount(starting_balance)
    ba.open_long('SP500', ba.check_balance() // adj_close_prices[start_pos], adj_close_prices[start_pos])
    ba.close_long('SP500', ba.check_holdings('SP500'), adj_close_prices[end_pos-1])
    if print_hist:
        print(ba.check_history())
    return ba.check_balance()

'''
moving_average_ranges_results = [(i, test_ma(moving_average_over=i)) for i in range(0, 2000, 10)]
moving_average_ranges_results.sort(key=lambda tup: tup[1])
print('Top 10:')
[print('ma' + str(tup[0]), '\t', str(int(tup[1]))) for tup in moving_average_ranges_results[-10:]]
print()
'''

ma200perf = test_ma(moving_average_over=200)
holdperf = test_buy_hold()
#print('ma50', '\t', int(test_ma(moving_average_over=50)))
#print('ma100', '\t', int(test_ma(moving_average_over=100)))
print('ma200', '\t', int(ma200perf))
print('hold', '\t', int(holdperf))
print()

print('Performance comparizon ')
#print('Best performing ('+ str(moving_average_ranges_results[-1][0]) + ') vs ma200:',
 #     moving_average_ranges_results[-1][1]/ma200perf)
print('ma200 vs hold:', ma200perf/holdperf)
