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

class OperativeSystemApp:
    def __init__(self):
        self.buffer = [0]*20
        self.lblBuffer = []
        self.producer = 0
        self.consumer = 0
        self.count = 0
        self.number = 0
        self.numbers = [3,4,5,6]
        self.still = Image.open("1.png")
        self.consuming = Image.open("2.png")
        self.producing = Image.open("3.png")
        self.still = self.still.resize((50, 50))
        self.producing = self.producing.resize((50, 50))
        self.consuming = self.consuming.resize((50, 50))
        
        self.operate()
        
    def operate(self):
        self.mainWindow()       

    def windowFormat(self):
        window = tk.Tk()
        window.title("Operative System")
        window.configure(background="#000000")
        window.geometry("1550x500")
        return window
    
    def keyHandler(self,key):
        if key.keycode == 27:
            self.window.destroy()
    
    def update(self):
        if self.count == self.number:
            self.count = 0
            
            index = self.producer-1
            if index < 0:
                index = 19
            self.img1.grid(row=1,column=index)
            
            index = self.consumer-1
            if index < 0:
                index = 19
            self.img2.grid(row=1,column=index)
            
            self.img3.grid_forget()
            self.img4.grid_forget()
            
            self.lbl1.config(text='Producer: -Resting- ')
            self.lbl2.config(text='Consumer: -Resting-')
        
        if self.count == 0:
            self.number = random.choice(self.numbers)
            
        if self.number % 2 == 0:
            if self.count == 0:
                self.img1.grid_forget()
                self.lbl1.config(text='Producer: >Producing< ')
                
            if self.buffer[self.producer] == 0:
                self.buffer[self.producer] = 1
                self.lblBuffer[self.producer].config(bg='#d7c7ff',text=str(self.producer+1).zfill(2),foreground='#000000')
                self.img3.grid(row=1,column=self.producer)
                self.producer += 1
            else:
                self.lbl1.config(text='Producer: >Waiting< ')
            
            if self.producer == 20:
                self.producer = 0
            
        else:
            if self.count == 0:
                self.img2.grid_forget()
                self.lbl2.config(text='Consumer: >Consuming<')
                
            if self.buffer[self.consumer] == 1:
                self.buffer[self.consumer] = 0
                self.lblBuffer[self.consumer].config(bg='#171717',text=str(self.consumer+1).zfill(2),foreground='#d7c7ff')
                self.img4.grid(row=1,column=self.consumer)
                self.consumer += 1
            else:
                self.lbl2.config(text='Consumer: >Waiting<')
        
            if self.consumer == 20:
                self.consumer = 0
        
        self.count += 1
        
        self.window.bind("<Key>",self.keyHandler)
                
        self.window.after(300, self.update)
        
    def mainWindow(self):
        self.window = self.windowFormat()

        self.lf1 = tk.LabelFrame(self.window, text="Producer - Consumer", padx=10, pady=10, font=('Century Gothic',14), bg="#000000", foreground='#d7c7ff')
        self.lf1.pack(pady=80)

        self.f1 = tk.LabelFrame(self.window,padx=10, pady=10,bg="#000000")
        self.f1.pack()

        for i in range(20):
            self.lbl = tk.Label(self.lf1,bg="#171717",text='  ', font=('Consolas',12), foreground='#d7c7ff', padx=10, pady=10, relief="groove", bd=2)
            self.lblBuffer.append(self.lbl)
            self.lbl.grid(row=0,column=i, padx=12, pady=12)
            
        self.lbl1 = tk.Label(self.f1,bg="#000000",text='Producer:', font=('Consolas',14), foreground='#d7c7ff')
        self.lbl1.grid(row=0,column=0)
        self.lbl2 = tk.Label(self.f1,bg="#000000",text='Consumer:', font=('Consolas',14), foreground='#d7c7ff')
        self.lbl2.grid(row=0,column=1)
        
        self.still = ImageTk.PhotoImage(self.still)
        self.producing = ImageTk.PhotoImage(self.producing)
        self.consuming = ImageTk.PhotoImage(self.consuming)
            
        self.img1 = tk.Label(self.lf1, image = self.still)
        self.img2 = tk.Label(self.lf1, image = self.still)
        self.img3 = tk.Label(self.lf1, image = self.producing)
        self.img4 = tk.Label(self.lf1, image = self.consuming)

        self.update()    
            
        self.window.mainloop()



# Execute program
if __name__ == "__main__":

    OperativeSystemApp()