import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
import yfinance as yf
import pandas as pd
import numpy as np 
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# exception handling variable 
exception = "Error:'/n'"
#################
# strategy functions 
"""
#RSI
def RSIcalc(asset, start, end):
    try:
        df = yf.download(asset, start=start, end=end)
    except:
        exception += "Make sure to input a valid ticker symbol./n Make sure Start date is before End Date./n"
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
"""
# MA Crossover
def movingAverageCalc(asset, start, end, ma1, ma2):
    try:
        df = yf.download(asset, start=start, end=end)
        
    except:
        exception += "Make sure to input a valid ticker symbol./n Make sure Start date is before End Date./n"
    df["MA" + str(ma1)] = df['Adj Close'].rolling(window=ma1).mean()
    df["MA" + str(ma2)] = df['Adj Close'].rolling(window=ma2).mean()

    df['Signal'] = np.where(df["MA" + str(ma1)] > df["MA" + str(ma2)], 1, 0)
    df['Position'] = df['Signal'].diff()

    df.loc[(df['Position'] == 1), 'Buy'] = "Yes"
    df.loc[(df['Position'] == -1), 'Buy'] = "Sell"
    
    df = df.dropna()
    return df

# MA
def movingAverage(asset, start, end, ma1):
    try:
        df = yf.download(asset, start=start, end=end)
    except:
        exception += "Make sure to input a valid ticker symbol./n Make sure Start date is before End Date./n"
    df["MA" + str(ma1)] = df['Adj Close'].rolling(window=ma1).mean()

    df['Signal'] = np.where(df["MA" + str(ma1)] > df['Adj Close'], 1, 0)
    df['Position'] = df['Signal'].diff()

    df.loc[(df['Position'] == 1), 'Buy'] = "Yes"
    df.loc[(df['Position'] == -1), 'Buy'] = "Sell"

    df = df.dropna()
    return df

# MACD
def MACD(asset, start, end, ma1, ma2):
    try:
        df = yf.download(asset, start=start, end=end)
    except:
        exception += "Make sure to input a valid ticker symbol./n Make sure Start date is before End Date./n"
    df["EMA" + str(ma1)] = df['Adj Close'].ewm(span=ma1).mean()
    df["EMA" + str(ma2)] = df['Adj Close'].ewm(span=ma2).mean()

    df['MACD Line'] = df["EMA" + str(ma1)] - df["EMA" + str(ma2)]
    df['Signal Line'] = df['MACD Line'].ewm(span=9).mean()

    df['Signal'] = np.where(df['MACD Line'] > df['Signal Line'], 1, 0)
    df['Position'] = df['Signal'].diff()

    df.loc[(df['Position'] == 1), 'Buy'] = "Yes"
    df.loc[(df['Position'] == -1), 'Buy'] = "Sell"

    return df

# get buying and selling dates 
def getSignals(df):
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)):
        if df["Buy"].iloc[i] == "Yes": 
            Buying_dates.append(df.iloc[i].name)
        elif df["Buy"].iloc[i] == "Sell":
            Selling_dates.append(df.iloc[i].name)
    return Buying_dates, Selling_dates

########################
#GUI Logic

# button pressed
def enter_data():

    # start date
    startDate = startCal.get_date()
    print(startDate)

    # end date
    endDate = endCal.get_date()
    print(endDate)

    # show sandp
    showSandP = sandpStatus.get()
    print(showSandP)

    # moving averages 
    ma1 = ma1Entry.get()
    ma2 = ma2Entry.get()
    # make sure mas are values
    try:
        ma1 = int(ma1)
        ma2 = int(ma2)
    except:
        exception += "There was a problem with the moving averages. Make sure to enter integers./n"
    
    # get security info 
    security = securityEntry.get().upper()
    print(security)
    try:
        df = yf.download(security, start=startDate, end=endDate)
        print(df.head)
    except:
        exception += "Make sure to input a valid ticker symbol./n Make sure Start date is before End Date./n"

    # strategy info
    strategy = clicked.get()
    print(strategy)

    # run selected strategy 
    #if strategy == "RSI":
    #    data = RSIcalc(security, startDate, endDate)
    #    buy, sell = getSignals(data)
    if strategy == "MA Crossover":
        data = movingAverageCalc(security, startDate, endDate, ma1, ma2)
        buy, sell = getSignals(data)
    elif strategy == "MA":
        data = movingAverage(security, startDate, endDate, ma1)
        buy, sell = getSignals(data)
    elif strategy == "MACD":
        data = MACD(security, startDate, endDate, ma1, ma2)
        buy, sell = getSignals(data)

    # make lists the same size
    if len(buy) > len(sell):
        buy.pop()
    elif len(sell) > len(buy):
        sell.pop()
    
    # create plot 
    fig = Figure(figsize=(12,5), dpi=90)
    plot1 = fig.add_subplot(111)
    


    # if checkbox is selected, plot s&p
    if showSandP == "Show S&P":
        dfSANDP = yf.download('SPY', start=startDate, end=endDate)
        plot1.plot(dfSANDP['Adj Close'], alpha = .75, label="S&P")
        #plt.plot(dfSANDP['Adj Close'], alpha = .01, label="S&P")
        #plt.legend()

    # calculate profits
    Profits = (data.loc[sell].Open.values - data.loc[buy].Open.values)/data.loc[buy].Open.values
    
    # winning rate 
    wins = [i for i in Profits if i >0]
    winRate = len(wins)/ len(Profits)

    # show profit and win rate
    profitLabel = tk.Label(frame, text="Profit: "+str(sum(Profits)))
    winRateLabel = tk.Label(frame, text="Win Rate: "+str(winRate))
    profitLabel.grid(row=4, column=0)
    winRateLabel.grid(row=5,column=0)

    # show graph 
    plot1.scatter(data.loc[buy].index, data.loc[buy]['Adj Close'], marker = '^', c='g')
    plot1.scatter(data.loc[sell].index, data.loc[buy]['Adj Close'], marker = 'v', c='r')
    plot1.plot(data['Adj Close'], alpha=1, label=security)
    plot1.legend()

    canvas1 = FigureCanvasTkAgg(fig, frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=3, column=0)


    
    
#####################
# GUI Elements
root = tk.Tk()

root.geometry("1200x800")
root.title("Backtester")

label = tk.Label(root, text="Select Security and Strategy", font=("ariel", 18))
label.pack(pady = 10)

frame = tk.Frame(root)
frame.pack()

# get security info
infoFrame = tk.LabelFrame(frame, text = "Strategy Information")
infoFrame.grid(row=0, column=0)



securityLabel = tk.Label(infoFrame, text="Security")
securityLabel.grid(row = 0, column = 0)
strategyLabel = tk.Label(infoFrame, text="Strategy")
strategyLabel.grid(row = 0, column=1)

# enter security and select strategy
securityEntry = tk.Entry(infoFrame)
clicked = StringVar()
clicked.set("MA")
strategySelect = OptionMenu(infoFrame, clicked, "MACD", "MA Crossover", "MA")
securityEntry.grid(row=1, column=0)
strategySelect.grid(row=1,column=1)

# start and end date calendars with labels
startLabel = tk.Label(infoFrame, text = "Start Date")
startLabel.grid(row=2, column=0)
endLabel = tk.Label(infoFrame, text = "End Date")
endLabel.grid(row=2, column=1)
startCal = DateEntry(infoFrame, selectmode= "day", year=2019, month=1, day=1)
startCal.grid(row=3, column=0)
endCal = DateEntry(infoFrame, selectmode= "day", year=2021, month=12, day=31)
endCal.grid(row=3, column=1)

# moving average inputs
ma1Label = tk.Label(infoFrame, text = "Moving Average 1")
ma2Label = tk.Label(infoFrame, text = "Moving Average 2")
ma1Label.grid(row=4, column=0, pady=5)
ma2Label.grid(row=4, column=1, pady=5)

ma1Entry = tk.Entry(infoFrame)
ma2Entry = tk.Entry(infoFrame)
ma1Entry.grid(row=5,column=0)
ma2Entry.grid(row=5,column=1)

# include s&p checkbox and button 
sandpStatus = tk.StringVar(value= "No S&P")
sandpCheck = tk.Checkbutton(frame, text="Show S&P 500 return", variable=sandpStatus, onvalue="Show S&P", offvalue="No S&P")
sandpCheck.grid(row=1,column=0)
runButton = tk.Button(frame, text = "Show Results", command=enter_data)
runButton.grid(row=2,column=0)

# show profit and win rate

root.mainloop()

