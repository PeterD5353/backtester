import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry

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

# start date calendar
cal = DateEntry(infoFrame, selectmode= "day", year=2021, month=12, day=31)
cal.grid(row=2, column=0)




# button pressed

root.mainloop()

