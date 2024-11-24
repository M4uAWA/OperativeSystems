# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 22:22:05 2024

@author: USER
"""
import random
import tkinter as tk
from PIL import ImageTk, Image

from ctypes import windll #IMPROVE RESOLUTION
windll.shcore.SetProcessDpiAwareness(1)

def windowFormat():
    window = tk.Tk()
    window.title("Operative System")
    window.configure(background="#000000")
    window.geometry("1550x500")
    return window

def keyHandler(key):
    if key.keycode == 27:
        window.destroy()

def update(buffer,producer,consumer,numbers,lblBuffer,count,number):
    if count == number:
        count = 0
        
        index = producer-1
        if index < 0:
            index = 19
        img1.grid(row=1,column=index)
        
        index = consumer-1
        if index < 0:
            index = 19
        img2.grid(row=1,column=index)
        
        img3.grid_forget()
        img4.grid_forget()
        
        lbl1.config(text='Producer: -Resting- ')
        lbl2.config(text='Consumer: -Resting-')
    
    if count == 0:
        number = random.choice(numbers)
        
    if number % 2 == 0:
        if count == 0:
            img1.grid_forget()
            lbl1.config(text='Producer: >Producing< ')
            
        if buffer[producer] == 0:
            buffer[producer] = 1
            lblBuffer[producer].config(bg='#d7c7ff',text=str(producer+1).zfill(2),foreground='#000000')
            img3.grid(row=1,column=producer)
            producer += 1
        else:
            lbl1.config(text='Producer: >Waiting< ')
        
        if producer == 20:
            producer = 0
        
    else:
        if count == 0:
            img2.grid_forget()
            lbl2.config(text='Consumer: >Consuming<')
            
        if buffer[consumer] == 1:
            buffer[consumer] = 0
            lblBuffer[consumer].config(bg='#171717',text=str(consumer+1).zfill(2),foreground='#d7c7ff')
            img4.grid(row=1,column=consumer)
            consumer += 1
        else:
            lbl2.config(text='Consumer: >Waiting<')
    
        if consumer == 20:
            consumer = 0
    
    count += 1
    
    window.bind("<Key>",keyHandler)
            
    window.after(300, lambda: update(buffer,producer,consumer,numbers,lblBuffer,count,number))

buffer = [0]*20
lblBuffer = []
producer = 0
consumer = 0
numbers = [3,4,5,6]
still = Image.open("1.png")
consuming = Image.open("2.png")
producing = Image.open("3.png")
count = 0
number = 0

still = still.resize((50, 50))
producing = producing.resize((50, 50))
consuming = consuming.resize((50, 50))

window = windowFormat()

still = ImageTk.PhotoImage(still)
producing = ImageTk.PhotoImage(producing)
consuming = ImageTk.PhotoImage(consuming)

lf1 = tk.LabelFrame(window, text="Producer - Consumer", padx=10, pady=10, font=('Century Gothic',14), bg="#000000", foreground='#d7c7ff')
lf1.pack(pady=80)

f1 = tk.LabelFrame(window,padx=10, pady=10,bg="#000000")
f1.pack()

for i in range(20):
    lbl = tk.Label(lf1,bg="#171717",text='  ', font=('Consolas',12), foreground='#d7c7ff', padx=10, pady=10, relief="groove", bd=2)
    lblBuffer.append(lbl)
    lbl.grid(row=0,column=i, padx=12, pady=12)
    
lbl1 = tk.Label(f1,bg="#000000",text='Producer:', font=('Consolas',14), foreground='#d7c7ff')
lbl1.grid(row=0,column=0)
lbl2 = tk.Label(f1,bg="#000000",text='Consumer:', font=('Consolas',14), foreground='#d7c7ff')
lbl2.grid(row=0,column=1)
    
img1 = tk.Label(lf1, image = still)
img2 = tk.Label(lf1, image = still)
img3 = tk.Label(lf1, image = producing)
img4 = tk.Label(lf1, image = consuming)

update(buffer,producer,consumer,numbers,lblBuffer,count,number)    
    
window.mainloop()