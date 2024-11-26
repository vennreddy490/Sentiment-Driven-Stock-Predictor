# Risk Free Rate is determined by the yield
# of a 10 Year treasury bond. The rate can
# be found at:
# https://treasurydirect.gov/marketable-securities/treasury-notes/
RISK_FREE_RATE = 4.2

# The number of trading days in a year (on average)
TRADING_DAYS = 252


# Calculate the daily risk-free rate
DAILY_RISK_FREE_RATE = (1 + (RISK_FREE_RATE / 100)) ** (1 / 365) - 1
