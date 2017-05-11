#!/usr/bin/python

import psutil
from tkinter import *
from tkinter import messagebox
import time
import sys

## Global Constants
title = "Process Suspender"
default_process = "example.exe"
default_pause = 5
pause_min = 1
pause_max = 10
button_w = 25
button_c = 'white'
img_path = 'logo.png'
font_param = ("Arial", 12, "bold")
relief_button = SOLID
width_switch = 10                   ## Width for the frame switch buttons
pad = 10
pad_text = 1

def getPIDFromName(name):
    for pid in psutil.pids():
        if psutil.Process(pid).name() == name:
            return pid
    raise ValueError("Process not found")

def resume():
    try:
        pid = getPIDFromName(process_name.get())
        psutil.Process(pid).resume()
        messagebox.showinfo( "Process", "The process has been resumed")
    except ValueError as err:
         messagebox.showinfo("Process","Process not found")

def suspend():
    try:
        pid = getPIDFromName(process_name.get())
        psutil.Process(pid).suspend()

        if auto_toggle.get() == 1:
            time.sleep(pause_time.get())
            resume()
        else:
            messagebox.showinfo( "Process", "The process has been suspended")
    except ValueError as err:
        messagebox.showinfo("Process","Process not found")

def raise_frame(frame):
    frame.tkraise()

if __name__ == "__main__":
    root = Tk()
    root.title(title)                                       ## Application Title
    process_name = StringVar(root, value = default_process)   ## Default process entry
    pause_time = IntVar(root, value = default_pause)                    ## Default pause time
    auto_toggle = IntVar(root, value=1)                     ## Default toggle value
    img = PhotoImage(file=img_path)                         ## Setting cover image

    ## Settings Frame
    settings = Frame(root)
    Button(settings,text='Main',command=lambda:raise_frame(main),font=font_param,relief=relief_button,width=width_switch,bg=button_c)\
            .grid(sticky="W",padx=pad,pady=pad)
    Label(settings, text="Process Name", font=font_param)\
            .grid(sticky=W,padx=pad,pady=pad_text)
    Entry(settings, textvariable=process_name,font=font_param)\
            .grid(row=1, column=1,sticky=E,padx=pad,pady=pad_text)
    Label(settings, text="Pause Time",font=font_param)\
            .grid(sticky=W,padx=pad,pady=pad_text)
    Spinbox(settings, textvariable=pause_time,font=font_param,from_=pause_min,to=pause_max)\
            .grid(row=2, column=1,sticky=E,padx=pad,pady=pad_text)
    Checkbutton(settings,text="Resume process after pause",variable=auto_toggle,onvalue=1,offvalue=0,font=font_param)\
            .grid(columnspan=2,sticky=W,padx=pad,pady=pad_text)

    ## Main Frame
    main = Frame(root)
    Button(main,text='Settings',command=lambda:raise_frame(settings),font=font_param,relief=relief_button,width=width_switch,bg=button_c)\
            .grid(sticky="W",padx=pad,pady=pad)
    Label(main,image=img)\
            .grid(sticky=N,columnspan=2,padx=pad,pady=pad)
    Button(main,text="Suspend",command=suspend,width=button_w,bg=button_c,font=font_param,relief=relief_button)\
            .grid(columnspan=2,padx=pad,pady=pad)
    Button(main,text="Resume",command=resume,width=button_w,bg=button_c,font=font_param,relief=relief_button)\
            .grid(columnspan=2,padx=pad,pady=pad)

    for frame in (settings, main):
        frame.grid(row=0, column=0, sticky='news')

    raise_frame(main)
    root.mainloop()
