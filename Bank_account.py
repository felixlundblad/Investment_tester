class BankAccount:
    def __init__(self, starting_capital: float = 0):
        self.balance = starting_capital
        self.holdings = {}

        # Holds transaction history. [Transaction number, Ticker, Buy/Sell, Volume, Price]
        self.history = []

    def open_long(self, ticker: str, volume: int, price: float) -> bool:
        if self.balance - price*volume > 0:
            if ticker in self.holdings.keys():
                self.holdings[ticker] += volume
            else:
                self.holdings[ticker] = volume
            self.balance -= volume*price
            self.history.append([len(self.history), ticker, 'B', volume, price])
            return True
        else:
            return False

    def close_long(self, ticker: str, volume: int, price: float) -> bool:
        if ticker in self.holdings.keys():
            self.holdings[ticker] -= volume
            self.balance += volume*price
            if self.holdings[ticker] == 0:
                self.holdings.pop(ticker)
        self.history.append([len(self.history), ticker, 'S', volume, price])

    def check_balance(self) -> float:
        return self.balance

    def check_holdings(self, ticker='none'):
        if ticker == 'none':
            return self.holdings
        else:
            return self.holdings[ticker] if ticker in self.holdings else 0

    def check_history(self, check_since_last=0):
        return str(self.history).replace('],', ']\n') if check_since_last == 0 else str(self.history[-check_since_last:]).replace('],', ']\n')
