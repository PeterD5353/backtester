# imports 
import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt

# define start and end dates (change later to textboxes)
start = "2011-01-01"
end = "2022-01-01"


# import data from wikipedia
tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]

# get list of all tickers 
tickers = tickers.Symbol.to_list()

# replace . with -
tickers = [i.replace(".", "-") for i in tickers]

###################################
# Strategies

# RSI 
def RSIcalc(asset):
    df = yf.download(asset, start='2011-01-01')
    df['MA200'] = df['Adj Close'].rolling(window=200).mean()
    df['price change'] = df['Adj Close'].pct_change()

    df["Upmove"] = df['price change'].apply(lambda x: x if x > 0 else 0)
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)

    df['avg Up'] = df['Upmove'].ewm(span=19).mean()
    df['avg Down'] = df['Downmove'].ewm(span=19).mean()

    df = df.dropna()

    df['RS'] = df['avg Up'] / df['avg Down']
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))
    df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = "Yes"
    df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = "No"
    return df

RSIcalc(tickers[0])

# Moving Average Crossover
# get moving average values
ma1 = 10
ma2 = 20


def movingAverageCalc(asset):
    df = yf.download(asset, start = start, end = end)
    df["MA" + str(ma1)] = df['Adj Close'].rolling(window=ma1).mean()
    df["MA" + str(ma2)] = df['Adj Close'].rolling(window=ma2).mean()

    df = df.dropna()








def getSignals(df):
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)):
        if "Yes" in df["Buy"].iloc[i]:
            Buying_dates.append(df.iloc[i+1].name)
            
            for j in range(1,11):
                if df['RSI'].iloc[i + j] > 40:
                    Selling_dates.append(df.iloc[i+j+1].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i+j+1].name)
    return Buying_dates, Selling_dates

frame = RSIcalc(tickers[0])
buy, sell = getSignals(frame)

plt.figure(figsize=(12,5))
plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker = '^', c='g')
plt.plot(frame['Adj Close'], alpha=.07)

# calculate profits
Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
Profits

# winning rate 
wins = [i for i in Profits if i >0]
len(wins)/ len(Profits)


movingAverageCalc(tickers[0])