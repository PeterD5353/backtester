from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

"""
# set user inputted variables 
commission = .003


# SMA strategy
class mySMAStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

backtest = Backtest(GOOG, mySMAStrategy, commission = commission, exclusive_orders=True)
stats = backtest.run()

print(stats)

"""

import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt

# import data from wikipedia
tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]

# get list of all tickers 
tickers = tickers.Symbol.to_list()

# replace . with -
tickers = [i.replace(".", "-") for i in tickers]