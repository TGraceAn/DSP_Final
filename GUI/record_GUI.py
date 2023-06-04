import tkinter as tk
from functools import partial
from tkinter import *

from numpy import record


root = tk.Tk()
root.geometry('1300x750')
root.resizable(width=False, height=False)

background = tk.PhotoImage(file="GUI/record_GUI_img/background_1_img.png")
label_background = tk.Label(root, image = background)
label_background.pack()


record_img = tk.PhotoImage(file="GUI/record_GUI_img/button/record_icon.png")
stop_record_img = tk.PhotoImage(file="GUI/record_GUI_img/button/stop_record_icon.png")
out_img = tk.PhotoImage(file="GUI/record_GUI_img/button/out_icon.png")
# ----------------------------------------------------------------------------
record_button = tk.Button(label_background, image = record_img, borderwidth=0, highlightthickness=0)
record_button.pack()


stop_record_button = tk.Button(label_background, image = stop_record_img, borderwidth=0, highlightthickness=0)
stop_record_button.pack_forget()


out_button = tk.Button(label_background, image = out_img, borderwidth=0, highlightthickness=0)

record_button.place(x = 400, y = 320)
# stop_record_button.place(x = 400, y = 470)


def start_recording():
    stop_record_button = tk.Button(label_background, image=stop_record_img, borderwidth=0, highlightthickness=0, command=stop_recording)
    stop_record_button.place(x=400, y=470)
    stop_record_button.pack()
    record_button.pack_forget()

def stop_recording():
    record_button = tk.Button(label_background, image=record_img, borderwidth=0, highlightthickness=0, command=start_recording)
    record_button.place(x=400, y=320)
    record_button.pack()
    stop_record_button.pack_forget()
    

root.mainloop()


