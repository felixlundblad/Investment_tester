from iexfinance.stocks import Stock
tsla = Stock('TSLA')
tsla.get_price()

from datetime import datetime
from iexfinance.stocks import get_historical_data

start = datetime(2017, 1, 1)
end = datetime(2018, 1, 1)

df = get_historical_data("TSLA", start, end, output_format='pandas')

import matplotlib.pyplot as plt

df.plot()
plt.show()
