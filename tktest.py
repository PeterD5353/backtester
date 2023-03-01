import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry

########################3
#Logic

# button pressed
def enter_data():
    # get security
    security = securityEntry.get().upper()
    print(security)

#####################
# GUI
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
options = StringVar()
options.set("Strategy")
strategySelect = OptionMenu(infoFrame, options, "RSI", "MA Crossover", "MA")
securityEntry.grid(row=1, column=0)
strategySelect.grid(row=1,column=1)

# start and end date calendars with labels
startLabel = tk.Label(infoFrame, text = "Start Date")
startLabel.grid(row=2, column=0)
endLabel = tk.Label(infoFrame, text = "Start Date")
endLabel.grid(row=2, column=1)
startCal = DateEntry(infoFrame, selectmode= "day", year=2021, month=12, day=31)
startCal.grid(row=3, column=0)
endCal = DateEntry(infoFrame, selectmode= "day", year=2019, month=1, day=1)
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

root.mainloop()

