# @title Programa 2 procesos generados automáticamente, id incremental, con ventanas submit
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:58:33 2024

@author: USER
"""

import random
import tkinter as tk
from tkinter import ttk
from process import Process
from batch import Batch
from queue import Queue

from ctypes import windll #IMPROVE RESOLUTION
windll.shcore.SetProcessDpiAwareness(1)

#Batch size for this program
bS = 5

def windowFormat():
    window = tk.Tk()
    window.title("Operative system")
    window.configure(background="#000000")
    window.geometry("1080x720")
    return window

def labelFormat(master,text):
    lbl = tk.Label(master, text=text, foreground='#d7c7ff', bg="#000000",justify=tk.CENTER, font=('Century Gothic',12))
    return lbl

def entryFormat(master,textVariable):
    entry = tk.Entry(master, textvariable = textVariable, bg="#e1d7fa", font=('Century Gothic',11, 'bold'),justify=tk.CENTER)
    return entry

def submitC():
    global entVar
    entVar = int(txtVar.get())
    window.destroy()
  
#for second program
def processCapture(batchQueue,auxBatch,tNew,operators):
    i = 0
    while (tNew != 0):

        auxProcess = Process()

        name = "Process" + str(i+1)
        meOma0 = int(random.randrange(1,2))
        auxProcess.name = name
        auxProcess.pid = i
        auxProcess.x = int(random.randrange(-99,99))
        auxProcess.operation = random.choice(operators)
        
        if(auxProcess.operation == "/" or auxProcess.operation == "%"):
            if(meOma0 == 1):
                auxProcess.y = int(random.randrange(1,99))
            else:
                auxProcess.y = int(random.randrange(-99,-1))
        else:
            auxProcess.y = int(random.randrange(-99,99))
        auxProcess.met = int(random.randrange(5,25))
        
        if(auxProcess.operation == "/"):
            auxProcess.result = round(auxProcess.x / auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "%"):
            auxProcess.result = round(auxProcess.x % auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "+"):
            auxProcess.result = round(auxProcess.x + auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "-"):
            auxProcess.result = round(auxProcess.x - auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "*"):
            auxProcess.result = round(auxProcess.x * auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        #Process enqueue

        if(auxBatch.processQueue.full()):     #When reaching batch size, enqueue batch
            batchQueue.put(auxBatch)
            auxBatch = Batch(bS)

        auxBatch.processQueue.put(auxProcess)

        i += 1
        tNew -= 1 #Decrement remaining processes

    if(not auxBatch.processQueue.empty()): #Case - Queuing an incomplete batch
        batchQueue.put(auxBatch)
    
    return batchQueue

#for second program  
def updateProgressbar():
    step = progressVar.get()
    step += 1
    if (step > 100):
        window.destroy()
        return
    progressVar.set(step)
    progressBar["value"] = step
    window.after(40, updateProgressbar)
    
    
#for second program
def keyHandler(key):
    global auxProcess
    global processArr
    global pauseCondition
    global timeT

    if(pauseCondition == False):

        if(int(key.keycode) == 69): #ERROR - E
            auxProcess.result = "ERROR"
            auxProcess.tE = auxProcess.met #Asign time elapsed the same value as met to trigger new process asignment

        elif(int(key.keycode) == 73): #INTERRUPTION - I
            auxProcess.tE = auxProcess.tE - 1
            processArr.append(auxProcess)
            auxProcess = processArr[0] #assign process currently being processed
            processArr.pop(0) #pop previous process from current batch process array

        elif(int(key.keycode) == 80): #PAUSE - P
            lf1.config(text="Paused")
            pauseCondition = True
            timeT = timeT - 1
            auxProcess.tE = auxProcess.tE - 1

    if(int(key.keycode) == 67): #CONTINUE - C
        lf1.config(text="Processing")
        pauseCondition = False
        timeT = timeT + 1
        auxProcess.tE = auxProcess.tE + 1

    return

def updateProcessing():
    global batchQueue
    global doneArr
    global processArr
    global auxProcess
    global batchCounter
    global timeT
    global pauseCondition
    global flag

    if(not timeT == 0):

        if(auxProcess.tE == auxProcess.met):
            if(not auxProcess.pid == None):
                doneArr.append(auxProcess)

            if(len(processArr) > 0):
                auxProcess = processArr[0] #assign process currently being processed
                processArr.pop(0) #pop it from current batch processes array

            else:
                flag = False

        if(len(processArr) == 0 and flag == False): #get new batch and fill processArr with current batch processes
            if (not batchQueue.empty()):
                currentBatch = batchQueue.get()

                batchCounter += 1
                batchNum = Process()
                batchNum.pid = ""
                batchNum.fullOpe = "- Batch number: " + str(batchCounter) +" -"
                batchNum.result = ""

                doneArr.append(batchNum)

                for i in range(currentBatch.processQueue.qsize()):
                    processArr.append(currentBatch.processQueue.get())

                auxProcess = processArr[0] #assign process currently being processed
                processArr.pop(0) #pop it from current batch processes array
                flag = True

        lbl01.config(text="\nNumber of pending batches: " + str(batchQueue.qsize()))

        processStr = ""
        for i in processArr:
            processStr = processStr + str(i.name)+ "    " +str(i.met) + "    " +str(i.tE) +"\n"
        lbl00.config(text=processStr)

        lbl1.config(text="ID: " + str(auxProcess.pid))
        lbl2.config(text="OP: " + str(auxProcess.fullOpe))
        lbl3.config(text="MET: " + str(auxProcess.met))
        lbl4.config(text="NAME: " + str(auxProcess.name))
        lbl5.config(text="TE: " + str(auxProcess.tE))
        lbl6.config(text="TR: " + str(auxProcess.met - auxProcess.tE))

        doneStr =""
        for i in doneArr:
          doneStr = doneStr + str(i.pid) + "    " + str(i.fullOpe) + "   " + str(i.result) + "\n"
        lbl9.config(text=doneStr)

        lbl10.config(text="Total time elapsed: "+str(timeT))

        if(pauseCondition == False):
            auxProcess.tE = auxProcess.tE + 1

    else:
        processArr.pop(0)
    
    if(pauseCondition == False):
        timeT = timeT + 1

    if(auxProcess.tE == auxProcess.met + 1):
        lbl1.config(text="ID: ")
        lbl2.config(text="OP: ")
        lbl3.config(text="MET: ")
        lbl4.config(text="NAME: ")
        lbl5.config(text="TE: ")
        lbl6.config(text="TR: ")
        return

    window.bind("<Key>", keyHandler) #keypress detection

    window.after(1000, updateProcessing)


#############################################Program start
window = windowFormat()

txtVar = tk.StringVar()
entVar = None

lbl = labelFormat(window,"\n\n\n\nHow many operations do you want to process?\n")
lbl.pack()

processEnt = entryFormat(window,txtVar)
processEnt.pack()

lbl = labelFormat(window,"")
lbl.pack()

sub = tk.Button(window,text='Submit', font=('Century Gothic',11), relief="flat", background='#e1d7fa', command=submitC)
sub.pack()

window.mainloop()


#Process capture

batchQueue = Queue()
auxBatch = Batch(bS)
tNew = entVar
operators = "+-*/%"
i = 0

batchQueue = processCapture(batchQueue,auxBatch,tNew,operators)

i = 0
window = windowFormat() #generating processes window

lbl = labelFormat(window,"\n\n\n\n\nGenerating operations...\n")
lbl.pack()

progressBarSyle = ttk.Style() #progressbar style
progressBarSyle.theme_use('clam')

progressBarSyle.configure("violet.Horizontal.TProgressbar",troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa",)

progressVar = tk.DoubleVar()
progressBar = ttk.Progressbar(variable=progressVar,length=250,maximum=100, style="violet.Horizontal.TProgressbar")
progressBar.pack()

updateProgressbar()

window.mainloop()



#End of first part



window = windowFormat()
displayProcess = Process()
auxProcess = displayProcess
processArr = []
processArr.append(displayProcess)
doneArr = [] #array to store finished processes (it is initialized here because they are permanent)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

timeT = 0
flag = False
batchCounter = 0
pauseCondition = False


#left panel


lbl01 = labelFormat(window,"\nNumber of Batches remaining: " + str(batchQueue.qsize()))
lbl01.grid(row=0, column=2)

lf0 = tk.LabelFrame(window, text="Curret Batch", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf0.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

lbl02 = labelFormat(lf0, "Name   MET    TE")
lbl02.pack()

lbl00 = tk.Label(lf0, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
lbl00.pack() #pending processes


#middle panel


lf1 = tk.LabelFrame(window, text="Processing", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf1.grid(row=1, column=1, padx=20, sticky=tk.NSEW)

lbl1 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl1.pack(anchor="w")
lbl2 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl2.pack(anchor="w")
lbl3 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl3.pack(anchor="w")
lbl4 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl4.pack(anchor="w")
lbl5 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl5.pack(anchor="w")
lbl6 = tk.Label(lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
lbl6.pack(anchor="w")


#right panel


lf2 = tk.LabelFrame(window, text="Done", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf2.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

lbl7 = labelFormat(lf2,"ID      OP    ANS")
lbl7.pack()

lbl9 = tk.Label(lf2, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
lbl9.pack() #done

lbl10 = tk.Label(window, text="Total time elapsed: 0",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')#done
lbl10.grid(row=2, column=2, padx=20)

updateProcessing()

window.mainloop()