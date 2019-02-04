from Bank_account import BankAccount

ba = BankAccount(100)

ba.open_long('XBT', 1, 10)
ba.close_long('XBT', 1, 100)

ba.open_long('APPL', 2, 20)
ba.open_long('ABB', 1, 30)
ba.open_long('NANO', 1, 3)
ba.open_long('ETH', 3, 1)
ba.open_long('RXP', 1, 2)

ba.close_long('ETH', 1, 10)

print(ba.check_balance())

print(ba.check_holdings())

print(ba.check_history())
print()
print(ba.check_history(4))
